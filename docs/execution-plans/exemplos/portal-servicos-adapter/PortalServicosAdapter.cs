// Infrastructure/ExternalServices/PortalServicos/PortalServicosAdapter.cs
using Application.Common;                 // Result<T>
using Application.Servicos.Models;        // SistemaInventario
using Infrastructure.ExternalServices.Common;
using Infrastructure.ExternalServices.PortalServicos.Mappers;
using Infrastructure.ExternalServices.PortalServicos.Models.Responses;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;

namespace Infrastructure.ExternalServices.PortalServicos;

/// <summary>
/// Adapter de integração com o inventário de sistemas do Portal de Serviços.
/// Herda de <see cref="HttpClientBase"/> (logging + serialização padronizados).
/// A resiliência (retry/circuit breaker/timeout) é aplicada no pipeline do HttpClient (ver DependencyInjection).
/// </summary>
public sealed class PortalServicosAdapter : HttpClientBase, IPortalServicosGateway
{
    private readonly PortalServicosSettings _settings;

    public PortalServicosAdapter(
        HttpClient httpClient,
        IOptions<PortalServicosSettings> settings,
        ILogger<PortalServicosAdapter> logger)
        : base(httpClient, logger)
    {
        _settings = settings.Value;

        // Autenticação de serviço (Bearer), quando aplicável.
        if (!string.IsNullOrWhiteSpace(_settings.ApiKey))
            SetBearerToken(_settings.ApiKey!);
    }

    public async Task<Result<IReadOnlyList<SistemaInventario>>> ObterSistemasAsync(
        CancellationToken ct = default)
    {
        var response = await GetAsync<InventarioApiResponse>(_settings.InventarioEndpoint, ct);

        if (!response.IsSuccess)
        {
            // Não lança: o Portal pode estar indisponível (RN-1.4).
            // O handler de GetSistemasDisponiveisQuery converte a falha em lista vazia.
            Logger.LogWarning(
                "Inventário do Portal indisponível. Status: {Status}, Erro: {Erro}",
                response.StatusCode, response.ErrorMessage);

            return Result.Error<IReadOnlyList<SistemaInventario>>(
                response.ErrorMessage ?? "Inventário do Portal de Serviços indisponível");
        }

        var sistemas = PortalServicosMapper.ToSistemasInventario(response.Data!);
        return Result.Success(sistemas);
    }
}
