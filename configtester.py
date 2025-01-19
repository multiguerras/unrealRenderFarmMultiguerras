import unreal # type: ignore

config_path = "/Game/Cinematics/GruposEscenas/REV1-2.REV1-2:MoviePipelineExecutorJob_6.DefaultConfig"
config_path = "/Game/Cinematics/SinAntianalising.SinAntianalising"

def print_configuration_details(config_path):
    """
    Imprime los detalles de una configuración de MoviePipelineConfig a partir de su path.

    :param config_path: Path del asset de configuración (ej: "/Game/Cinematics/MyConfig")
    """
    # Cargar el asset de configuración
    config_asset = unreal.EditorAssetLibrary.load_asset(config_path)
    
    if not config_asset:
        print(f"No se pudo cargar el asset de configuración en la ruta: {config_path}")
        return

    # Verificar si el asset es una configuración válida
    if not isinstance(config_asset, (unreal.MoviePipelineMasterConfig, unreal.MoviePipelinePrimaryConfig)):
        print(f"El asset en {config_path} no es una configuración válida de MoviePipeline.")
        return

    print(f"Detalles de la configuración: {config_path}")
    print("=" * 50)

    # Imprimir propiedades básicas
    print(f"Nombre de la configuración: {config_asset.get_name()}")
    print(f"Clase de la configuración: {config_asset.get_class().get_name()}")

    # Obtener y imprimir los ajustes (settings) de la configuración
    settings = config_asset.get_all_settings()
    for setting in settings:
        print("\nAjuste:")
        print(f"  Clase: {setting.get_class().get_name()}")
        print(f"  Nombre: {setting.get_name()}")
        
        # Usar `dir()` para inspeccionar los atributos del ajuste
        print("  Propiedades disponibles:")
        for attr in dir(setting):
            if not attr.startswith("_"):  # Filtrar atributos privados
                print(f"    {attr}")

    print("=" * 50)

if __name__ == '__main__':
    print_configuration_details(config_path)