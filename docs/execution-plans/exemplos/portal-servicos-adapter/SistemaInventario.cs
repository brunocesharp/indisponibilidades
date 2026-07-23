// Application/Servicos/Models/SistemaInventario.cs
namespace Application.Servicos.Models;

/// <summary>
/// Sistema disponível no inventário do Portal de Serviços (modelo de leitura da Application).
/// </summary>
public sealed record SistemaInventario(string Codigo, string Sigla, string Nome);
