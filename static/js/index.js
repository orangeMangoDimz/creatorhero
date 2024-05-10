const reconstructStringJSON = (str) => {
    const jsonString = str.replace(/'/g, '"') 
    const jsonArray = JSON.parse(jsonString)
    return jsonArray
}

  let getChart = document.getElementById("chart");
  const chart_draw = getChart.getContext("2d");
  let labels = getChart.getAttribute("data-labels")
  let chart_data = getChart.getAttribute("data-chart_dat")
  labels = reconstructStringJSON(labels)
  chart_data = reconstructStringJSON(chart_data)
  console.log(labels)
  console.log(chart_data)
  let chart = new Chart(chart_draw, {
    type: "bar",
    data: {
      labels: labels,
       datasets: [
          {
            label: "Jumlah Subscribers",
            backgroundColor: "#79AEC8",
            borderColor: "#417690",
            data: chart_data,
          }
       ]
    },
    options: {
       title: {
          text: "Total Subscribers 4 Minggu Terakhir",
          display: true
       }
    }
  });