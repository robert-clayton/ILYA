$files = ( Get-ChildItem -Recurse "Images" | ForEach-Object FullName | Where-Object { $_ -match "png$" } ) 
$length = $files.Length
For ( $i = 1; $i -le $length; ++$i ) {
    $file = $files[$i - 1]  
    echo "Working on file $i of ${length}: $file"
    magick convert $file $file
}