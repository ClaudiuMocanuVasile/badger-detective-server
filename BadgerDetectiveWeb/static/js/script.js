window.onload = main;

function main()
{
	console.log("Gab was here");

	// CSRF token

	function getCSRFToken(name) {
		let cookieValue = null;
		if (document.cookie && document.cookie !== "") {
			const cookies = document.cookie.split(";");
			for (let i = 0; i < cookies.length; i++) {
				const cookie = cookies[i].trim();

				if (cookie.substring(0, name.length + 1) === name + "=") {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	}
	var csrftoken = getCSRFToken("csrftoken");
	clear_input();
}

function do_the_graph(data)
{
    // var data = "{{rows|safe}}"
    if(document.getElementById("output"))
    {
        
        data = data.replaceAll("(", "[").replaceAll(")", "]").replaceAll("'", '"').replaceAll("-", "/")
        data = JSON.parse(data)

        graph_date_as_string = Array()
        graph_prices = Array()

        for(let i = 0; i < data.length; i += 1)
        {
            data[i].push(data[i][0])
            graph_date_as_string.push(data[i][2])
            data[i][0] = data[i][0].split("/")
            data[i][0] = data[i][0][1] + "/" + data[i][0][0] + "/" + data[i][0][2]

            if(Number.isInteger(data[i][1]))
            {
                data[i][1] = data[i][1].toString() + ".00"
                graph_prices.push(parseInt(data[i][1]))
            }
            else
                {
                    if(data[i][1].toString().split(".")[1].length == 1)
                        data[i][1] = data[i][1].toString() + "0"
                    else
                        data[i][1] = data[i][1].toString()
                        
                    graph_prices.push(parseFloat(data[i][1]))
                }
        }

        string = ""
        
        for(let i = 0; i < data.length - 1; i += 1)
        {
            console.log(data[i])   
            let x = new Date(data[i][0])
            let y = new Date(data[i + 1][0])

            const diffTime = Math.abs(x - y);
            const days = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

            if(days == 1)
                string += data[i][1] + " RON pe " + data[i][2] + ".<br>"
            else
                string += data[i][1] + " RON intre " + data[i][2] + " si " + data[i+1][2] + ".<br>"
        }

        string += data[data.length - 1][1] + " RON de pe " + data[data.length - 1][2] + ".<br>"

        const ctx = document.getElementById('chart').getContext('2d');

        const myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: graph_date_as_string,
                datasets: [{
                    label: 'Price over time',
                    data: graph_prices,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)'
                    ],
                    borderWidth: 1
                }]
            },
        });
        document.getElementById("output").innerHTML = string
    }
}

function clear_input() {
	let button = document.getElementById("ob");
	button.onclick = () => {
		let input = document.getElementById("id_link");
		input.value= "";
		console.log(input);
	}
}
