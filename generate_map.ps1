Get-ChildItem -Path "assets" -Directory | ForEach-Object { 
    $img = Get-ChildItem -Path $_.FullName -Include *.png, *.jpg -Recurse | Select-Object -First 1
    if ($img) { "$($_.Name)|assets/$($_.Name)/$($img.Name)" }
} | Out-File -FilePath image_map.txt -Encoding UTF8
