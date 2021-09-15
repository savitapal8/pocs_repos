resource "google_compute_snapshot" "snapshot" {
  project = var.project_id
  name        = var.name
  source_disk = var.source_disk_name
  zone        = var.zone
  storage_locations = var.location
}