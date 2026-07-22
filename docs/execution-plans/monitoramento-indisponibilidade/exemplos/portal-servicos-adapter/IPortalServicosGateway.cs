// Infrastructure/ExternalServices/PortalServicos/IPortalServicosGateway.cs
using Application.Common; // Result<T>
using Application.Servicos.Models; // SistemaInventario

namespace Infrastructure.ExternalServices.PortalServicos;

/// <summary>
/// Gateway de acesso ao inventário de sistemas do Portal de Serviços.
/// Este sistema NÃO gerencia o cadastro de sistemas — apenas consome (RN-1.1).
/// </summary>
public interface IPortalServicosGateway
{
    /// <summary>
    /// Retorna a lista de sistemas cadastrados no inventário do Portal.
    /// Em caso de indisponibilidade do Portal, retorna Result de falha —
    /// cabe ao handler tratar como lista vazia (RN-1.4 / Cenário 1.4).
    /// </summary>
    Task<Result<IReadOnlyList<SistemaInventario>>> ObterSistemasAsync(
        CancellationToken ct = default);
}
