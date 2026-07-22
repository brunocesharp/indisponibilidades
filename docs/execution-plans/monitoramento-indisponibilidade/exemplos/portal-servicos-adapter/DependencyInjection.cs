// Infrastructure/ExternalServices/DependencyInjection.cs (trecho relativo ao Portal)
using Infrastructure.ExternalServices.PortalServicos;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Polly; // DelayBackoffType

namespace Infrastructure.ExternalServices;

public static class DependencyInjection
{
    public static IServiceCollection AddExternalServices(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        services.Configure<PortalServicosSettings>(
            configuration.GetSection(PortalServicosSettings.SectionName));

        var settings = configuration
            .GetSection(PortalServicosSettings.SectionName)
            .Get<PortalServicosSettings>()!;

        services
            .AddHttpClient<IPortalServicosGateway, PortalServicosAdapter>(client =>
            {
                client.BaseAddress = new Uri(settings.BaseUrl);
                client.Timeout = TimeSpan.FromSeconds(settings.TimeoutSeconds);
                client.DefaultRequestHeaders.Add("Accept", "application/json");
            })
            // Microsoft.Extensions.Http.Resilience — encapsula Polly v8
            .AddStandardResilienceHandler(options =>
            {
                options.Retry.MaxRetryAttempts = settings.MaxRetryAttempts;
                options.Retry.Delay = TimeSpan.FromMilliseconds(settings.RetryBaseDelayMs);
                options.Retry.BackoffType = DelayBackoffType.Exponential;
                options.Retry.UseJitter = true;

                options.CircuitBreaker.SamplingDuration = TimeSpan.FromSeconds(30);
                options.CircuitBreaker.FailureRatio = 0.5;
                options.CircuitBreaker.MinimumThroughput = 10;
                options.CircuitBreaker.BreakDuration = TimeSpan.FromSeconds(30);

                options.AttemptTimeout.Timeout = TimeSpan.FromSeconds(settings.AttemptTimeoutSeconds);
                options.TotalRequestTimeout.Timeout = TimeSpan.FromSeconds(settings.TimeoutSeconds);
            });

        return services;
    }
}
