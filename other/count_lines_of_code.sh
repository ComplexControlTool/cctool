git ls-files | grep -v ".json\|.gif\|.png\|.otf\|.eot\|.svg\|.ttf\|.woff\|.woff2\|.ico\|.jpg\|.min.js" | xargs wc -l