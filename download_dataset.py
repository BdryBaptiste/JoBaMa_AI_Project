from picsellia import Client
from picsellia.types.enums import AnnotationFileType
from dynaconf import Dynaconf
from pathlib import Path

base_dir = Path(__file__).resolve().parent
settings = Dynaconf(settings_files=[base_dir / "config.toml"])


def download_images_and_annotations():
    client = Client(
        api_token=settings.api_token,
        host=settings.host,
        organization_name=settings.orga
    )

    # Accès au projet et à l'expérience
    dataset = client.get_dataset_by_id(settings.dataset_id)
    versions = dataset.list_versions()

    if not versions:
        print("Aucun version de dataset trouvée.")
        return

    version = versions[-1]  # on prend la dernière version
    dataset_dir = Path(settings.output_dir) / dataset.name
    dataset_dir.mkdir(parents=True, exist_ok=True)

    print(f"Dataset: {dataset.name}")
    print(f"Version: {version.name}")

    # Télécharger les assets (images)
    print("⬇Téléchargement des images...")
    assets = version.list_assets()
    assets.download(str(dataset_dir / "images"))

    # Exporter les annotations au format COCO
    print("Export des annotations au format COCO...")
    version.export_annotation_file(
        annotation_file_type=AnnotationFileType.YOLO, target_path=str(dataset_dir)
    )

    print(f"Téléchargement terminé dans : {dataset_dir}")


if __name__ == "__main__":
    download_images_and_annotations()