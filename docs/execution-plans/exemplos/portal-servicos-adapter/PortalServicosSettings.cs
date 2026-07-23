// Infrastructure/ExternalServices/PortalServicos/PortalServicosSettings.cs
namespace Infrastructure.ExternalServices.PortalServicos;

/// <summary>
/// Configuração do adapter de inventário do Portal de Serviços.
/// Preenchida via appsettings (seção "ExternalServices:PortalServicos").
/// </summary>
public class PortalServicosSettings
{
    public const string SectionName = "ExternalServices:PortalServicos";

    /// <summary>URL base da API do Portal de Serviços.</summary>
    public string BaseUrl { get; set; } = string.Empty;

    /// <summary>Caminho do endpoint que lista o inventário de sistemas.</summary>
    public string InventarioEndpoint { get; set; } = "/api/v1/sistemas";

    /// <summary>Token/chave de serviço para autenticação (Bearer). Opcional se via SSO.</summary>
    public string? ApiKey { get; set; }

    // Timeouts (usados também pela pipeline de resiliência)
    public int TimeoutSeconds { get; set; } = 30;
    public int AttemptTimeoutSeconds { get; set; } = 10;

    // Retry / Circuit breaker
    public int MaxRetryAttempts { get; set; } = 3;
    public int RetryBaseDelayMs { get; set; } = 500;
}
