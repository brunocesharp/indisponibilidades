// Application/Servicos/Queries/GetSistemasDisponiveis/GetSistemasDisponiveisQueryHandler.cs
using Application.Servicos.Models;
using Infrastructure.ExternalServices.PortalServicos;
using MediatR;

namespace Application.Servicos.Queries.GetSistemasDisponiveis;

public sealed record GetSistemasDisponiveisQuery
    : IRequest<IReadOnlyList<SistemaInventario>>;

/// <summary>
/// Retorna os sistemas do inventário do Portal que ainda NÃO estão no monitoramento (RN-1.1).
/// Se o Portal estiver indisponível, retorna lista vazia (RN-1.4 / Cenário 1.4).
/// </summary>
public sealed class GetSistemasDisponiveisQueryHandler
    : IRequestHandler<GetSistemasDisponiveisQuery, IReadOnlyList<SistemaInventario>>
{
    private readonly IPortalServicosGateway _portal;
    private readonly IServicoMonitoradoRepository _servicos;

    public GetSistemasDisponiveisQueryHandler(
        IPortalServicosGateway portal,
        IServicoMonitoradoRepository servicos)
    {
        _portal = portal;
        _servicos = servicos;
    }

    public async Task<IReadOnlyList<SistemaInventario>> Handle(
        GetSistemasDisponiveisQuery request,
        CancellationToken ct)
    {
        var resultado = await _portal.ObterSistemasAsync(ct);

        // RN-1.4: inventário indisponível → lista vazia (a tela exibe vazio).
        if (!resultado.IsSuccess)
            return Array.Empty<SistemaInventario>();

        // RN-1.1: remove os que já estão monitorados.
        var codigosMonitorados = await _servicos.ObterCodigosSistemaAsync(ct);

        return resultado.Value
            .Where(s => !codigosMonitorados.Contains(s.Codigo))
            .ToList();
    }
}
