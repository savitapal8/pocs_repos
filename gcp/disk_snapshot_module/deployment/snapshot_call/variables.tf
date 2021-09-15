variable "zone" {
  type = "string"
  default = "us-central1-a"
}

variable "name" {
  type="string"
  default ="snap"
}

variable "disk_count" {
  type = "number"
  default = 5
}

variable "location"{
    type="string"
    default = "us-central1"
}

variable "source_disk_name"{
    type="string"
    default = "disk1"
}

variable "project_id"{
    type="string"
    default =  "sunnywale-project"
}