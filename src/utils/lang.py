def lang(fname):
    exts = {
        "py" : "python",
        "c" : "c",
        "cpp" : "c++",
        "js" : "javascript",
        "html" : "html",
        "css" : "css",
        "md" : "md",
        "png" : "png",
        "jpg" : "jpg",
    }
    tmp = fname.split(".")
    ext = tmp[len(tmp)-1]
    if ext in exts :
        return exts[ext]
    else :
        return "plain"