
function GenerateResult(csvData) {

    var divSearchResult = document.getElementById("search-result");
    var divRow = document.createElement("div");
    console.log(csvData);
    var cmpt = 0;
    var isDone = false;

    while (!isDone) {
        for (j = 0; j < 4; j++) {
            ///creer tag
            var divCard = document.createElement("div");
            var divColumn = document.createElement("div");
            var divPrice = document.createElement("h5");
            var a = document.createElement('a');
            var divImg = document.createElement("img");
            

            //logique
                if (typeof csvData[cmpt][j] !== ('undefined' || "")) {
                    let title = csvData[cmpt][0];
                    var linkText = document.createTextNode(title);
                    let price = csvData[cmpt][1].concat(',', csvData[cmpt][2]);
                    let url = csvData[cmpt][3]
                    linkText.innerText = title;
                    divPrice.innerText = price;
                    a.href = url;
                }
            

            divCard.classList.add("card");
            divColumn.classList.add("column");

            document.body.appendChild(a);
            a.appendChild(linkText);
            divCard.appendChild(a);
            divCard.appendChild(divPrice);
            divColumn.appendChild(divCard);
            divRow.appendChild(divColumn);

            if (csvData.length - cmpt == 1) {
                isDone = true;
                break;
            }

            cmpt++;
        }

        divRow.classList.add("row");

        divSearchResult.appendChild(divRow);
    }

}


window.onload = (event) => {
    var request = new XMLHttpRequest();
    const open_file = request.open("GET", "../../crawler copy/output.json", false);
    request.send(null);

    var jsonData = new Array();

    fetch("../../crawler copy/output.json").then(response => {
        return response.json();
    }).then(jsondata => {
        for (var i = 0; i < jsondata.item.length; i++) {
            var Temp = new Array(jsondata.item[i].title, jsondata.item[i].price, jsondata.item[i].link);
            jsonData.push(Temp);
        }
        GenerateResult(jsonData);
    });
};

function formatData(request){
    var csvData = new Array();
    var jsonObject = request.responseText.split("\n");

    for (var i = 1; i < jsonObject.length - 1; i++) {
        csvData.push(jsonObject[i].split(','));
    }

    console.log(csvData)

    for (var i = 0; i < csvData.length; i++) {
        for (var j = 0; j < csvData[i].length; j++) {
            csvData[i][j] = csvData[i][j].replace("\"", '').replace("\\", '');
        }
    }

    return csvData;
}

function searchItems(event){
    const keyName = event.key;
    var inputContent = document.getElementsByClassName("form-control")[0];
    var titleSearch = document.getElementsByClassName("bestSellers")[0];

    if(keyName ==  "Enter" && inputContent.value !==""){

        titleSearch.innerText ="Search Result";

        console.log(inputContent.value);

        var request = new XMLHttpRequest();
        request.onload = function() {
            csvData = formatData(request);
            GenerateResult(csvData);
        }
        request.open("GET", "../../crawler/output.csv", false);
        request.send(null);

    }
}

document.addEventListener('keydown',searchItems);