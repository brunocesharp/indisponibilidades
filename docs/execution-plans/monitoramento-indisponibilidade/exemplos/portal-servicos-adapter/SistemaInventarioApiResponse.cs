// Infrastructure/ExternalServices/PortalServicos/Models/Responses/SistemaInventarioApiResponse.cs
namespace Infrastructure.ExternalServices.PortalServicos.Models.Responses;

/// <summary>
/// Envelope da resposta do endpoint de inventário do Portal.
/// Ajustar aos nomes reais do contrato (pendente em refinement-api).
/// </summary>
public sealed record InventarioApiResponse
{
    public IReadOnlyList<SistemaInventarioApiResponse> Sistemas { get; init; }
        = Array.Empty<SistemaInventarioApiResponse>();
}

/// <summary>
/// Item de sistema retornado pelo Portal de Serviços.
/// </summary>
public sealed record SistemaInventarioApiResponse
{
    public string Codigo { get; init; } = string.Empty;
    public string Sigla { get; init; } = string.Empty;
    public string Nome { get; init; } = string.Empty;
}
