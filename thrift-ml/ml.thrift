struct FileData {
    1:string name,
    2:binary buff
}

service Filebuff {
    string predict(1:FileData file)
}