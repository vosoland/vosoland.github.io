function find(searchVal, bgColor) {
    var oDiv = document.getElementsByTagName("body")[0];
    var sText = oDiv.innerHTML;
    var reg1 = /<script[^>]*>(.|\n)*<\/script>/gi; //去掉script标签 
    sText = sText.replace(reg1, "");
    var bgColor = bgColor || "orange";
    var num = -1;
    var rStr = new RegExp(searchVal, "gi"); //匹配传入的搜索值不区分大小写 i表示不区分大小写，g表示全局搜索
    var rHtml = new RegExp("\<.*?\>", "ig"); //匹配html元素
    var aHtml = sText.match(rHtml); //存放html元素的数组
    var arr = sText.match(rStr);
    a = -1;
    sText = sText.replace(rHtml, '{~}'); //替换html标签
    sText = sText.replace(rStr, function () {
        a++;
        return "<span name='addSpan' style='background-color: " + bgColor + ";'>" + arr[a] + "</span>"
    }); //替换key
    sText = sText.replace(/{~}/g, function () { //恢复html标签
        num++;
        return aHtml[num];
    });
    oDiv.innerHTML = sText;
}

find(`{ key }`)