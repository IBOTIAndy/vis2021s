var title = "treemap";


function dataLoader(text,cb) {
	//有些csv資料的seperator是使用分號，這邊統一使用逗號座分隔
    var uri = 'data:text/plain;base64,' + Base64.encode(text.replace(/;/g, ','))
    var dsv = d3.dsvFormat(",")

    d3.csv(uri, function(rawData){
        //做資料處理，csv中有些資料是字串，不是數字形式，要轉成數字
        csvData = rawData.map(function(d){
            var t = {}

            for (var k in d) {
                
                //把字串轉成number
                if(/[0-9]+/.test(d[k])){
                    t[k] = parseInt(d[k].replace(/(,|\s)+/g, ''))
                }
                //-符號代表為0
                else if(d[k].replace(/^\s+|\s+$/g, '') == '-'){
                    t[k] = 0
                }
                //在本題中，因為有欄位是空的，空的欄位設置為0
                else if(d[k].length == 0){
                    t[k] = 0
                }
                //不是數字就不處理
                else {
                    t[k] = d[k]
                }
            }
            return t
        })

        if (!csvData.length){			
			return
		}
            
		
		//獲取html中的下拉式選單
		//只要使用者更改選單欄位，就會用不同的欄位做為分層
        var objectKeys = document.getElementById("ObjectKeys")
		for(var k in csvData[0]){
			objectKeys.add(new Option(k, k))
		}
	
		cb()
    })
}

function dataClassifier(key, callback) {
	
	var makeMapping = function(mappingRange){
		var flatten = []
		
		var correspondingMapping = {}
		
		//將所有數值取出置入faltten中
		for(var i = 0; i<csvData.length; i++){
			for(var j in csvData[i]){
				if(typeof csvData[i][j] == "number"){
					correspondingMapping[csvData[i][j]] = null
					flatten.push(csvData[i][j])
				}
			}
		}
		
		flatten = flatten.sort(function(a,b){
			return a - b
		})
		//數值映射公式
		//假設原本的區間為Omin~Omax，對應的區間為Nmin~Nmax
		//公式為Nmapping = [(Nmax-Nmin) / (Omax-Omin) * (O-Omin)] + Nmin
		for(var k in correspondingMapping){
			correspondingMapping[k] = ((mappingRange[1] - mappingRange[0]) / (flatten[flatten.length - 1] - flatten[0])) * (parseFloat(k) - flatten[0]) + mappingRange[0]	
		}
		
		return correspondingMapping
	}
	
	//將原有數值對應到較小的區間
	var mapping = makeMapping([20, 100])

    var d3json = {
        children: [],
        name: title
    }

	var layer = []
	//循環讀取所有的data
    csvData.forEach(function(d){
		//這邊讀取所有非分層的名稱，只要該名稱不是分層名字就加入子節點中
		//比如你想用 類別 作為分層名稱，那就把除了類別的名稱加入子節點	
		var list = []
		for(var k in d){
			if(k != key){
				list.push(k)
			}
		}
		
		//這邊將所有的分層名稱加入至layer陣列中
        layer.push(d[key])

        //以單位名稱作為分曾
        d3json.children.push({
            name: d[key],
            children: list.map(function(k){
                //代表每一個長方形的大小
				//如果直接以節點本身的數值計算長方形大小，可能會因為不同節點的數值差異過大
				//而導致有些長方形面積很大，有些很小，會有很多長方形湖在一起
                return {
                    name: k,
                    size: mapping[d[k]],
                    value: d[k]
                }
            })
        })
    })

    callback(d3json, layer)
}