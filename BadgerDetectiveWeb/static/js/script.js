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
}

function do_the_graph(data)
{
    // var data = "{{rows|safe}}"
    if(document.getElementById("output"))
    {
        data = data.slice(1, data.length - 1)
        data = data.split(", ")

        string = ""

        graph_date_as_string = Array()
        graph_date = Array()
        graph_prices = Array()

        for(let i = 0; i < data.length; i += 2)
        {

            data[i] = data[i].slice(2, data[i].length - 1)
            let tmp = data[i].split("-")
            data[i] = tmp[1] + "-" + tmp[0] + "-" + tmp[2]
            graph_date_as_string.push(data[i])
            data[i+1] = data[i+1].slice(0, data[i+1].length - 1)
            data[i] = new Date(data[i])
            graph_date.push(data[i])
            graph_prices.push(parseFloat(data[i+1]))
            let d = data[i].getDate()
            let m = data[i].getMonth() + 1
            let y = data[i].getFullYear()
            
            if( i > 0 && i < data.length - 1)
            {
                let tmp = new Date(data[i])
                tmp.setDate(tmp.getDate() - 1)
                tmp = new Date(tmp)
                let d = tmp.getDate()
                let m = tmp.getMonth() + 1
                let y = tmp.getFullYear()
                string += d + "/" + m + "/" + y + ".<br>"
            }
            if( i == data.length - 2)
            {
                string += data[i+1] + " RON as of " + d + "/" + m + "/" + y + "."
            }
            else
            {
                string += data[i+1] + " RON from " + d + "/" + m + "/" + y + " to "
            }
        }
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
