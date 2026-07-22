// Infrastructure/ExternalServices/PortalServicos/Mappers/PortalServicosMapper.cs
using Application.Servicos.Models;
using Infrastructure.ExternalServices.PortalServicos.Models.Responses;

namespace Infrastructure.ExternalServices.PortalServicos.Mappers;

/// <summary>
/// Converte os modelos da API do Portal nos modelos consumidos pela Application.
/// Mantém a Application isolada do contrato externo.
/// </summary>
public static class PortalServicosMapper
{
    public static IReadOnlyList<SistemaInventario> ToSistemasInventario(InventarioApiResponse api)
        => api.Sistemas
            .Select(s => new SistemaInventario(
                Codigo: s.Codigo,
                Sigla: s.Sigla,
                Nome: s.Nome))
            .ToList();
}
