$jobs = @()

Write-Host "Starting port-forwarding for Django App (8000:80)..."
$jobs += Start-Job -ScriptBlock { kubectl port-forward svc/django-service 8000:80 }

Write-Host "Starting port-forwarding for Grafana (3000:3000)..."
$jobs += Start-Job -ScriptBlock { kubectl port-forward svc/grafana-service 3000:3000 }

Write-Host "Starting port-forwarding for Prometheus (9090:9090)..."
$jobs += Start-Job -ScriptBlock { kubectl port-forward svc/prometheus-service 9090:9090 }

Write-Host "Port forwarding started. Press Ctrl+C to stop."

try {
    while ($true) {
        foreach ($job in $jobs) {
            Receive-Job -Job $job -Keep
        }
        Start-Sleep -Seconds 2
    }
}
finally {
    Write-Host "Stopping port-forwarding..."
    foreach ($job in $jobs) {
        Stop-Job -Job $job
        Remove-Job -Job $job
    }
}
