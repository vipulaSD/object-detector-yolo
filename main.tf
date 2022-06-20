provider "google" {
    project = "detector-353911"
}

resource "google_cloud_run_service" "default" {
    name     = "cloud_run"
    location = "us-central1"

    metadata {
      annotations = {
        "run.googleapis.com/client-name" = "terraform"
      }
    }

    template {
      spec {
        containers {
          image = "gcr.io/detector-353911/detector"
        }
      }
    }
 }

 data "google_iam_policy" "noauth" {
   binding {
     role = "roles/run.invoker"
     members = ["allUsers"]
   }
 }

 resource "google_cloud_run_service_iam_policy" "noauth" {
   location    = google_cloud_run_service.default.location
   project     = google_cloud_run_service.default.project
   service     = google_cloud_run_service.default.name
   policy_data = data.google_iam_policy.noauth.policy_data
}