module "disk_snapshot" {
    count = var.disk_count
    source = "../../module/snapshot"
    project = var.project_id
    name        = "${var.name}-${count.index}" 
    source_disk = var.source_disk_name
    zone        = var.zone
    storage_locations = var.location
}