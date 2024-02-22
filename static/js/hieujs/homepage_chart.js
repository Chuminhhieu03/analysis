// create a chart line for homepage with id canvas is "lineChartMonth"
function createLineChartMonth(datathismonth, datalastmonth) {
  var ctx = document.getElementById("lineChartMonth").getContext("2d");
  var lineChartMonth = new Chart(ctx, {
    type: "line",
    data: {
      labels: ["0", "5", "10", "15", "20", "25", "30"],
      datasets: [
        {
          label: "Tháng này",
          data: [0, 10, 5, 2, 20, 30, 45],
          backgroundColor: "rgba(83, 109, 220, 0.2)",
          borderColor: "rgba(83, 109, 220, 1)",
          pointStyle: "circle",
          borderWidth: 1,
          pointStyle: "circle",
        },
        {
          label: "Tháng trước",
          data: [0, 5, 2, 8, 15, 25, 30],
          backgroundColor: "rgba(82, 205, 255, 0.2)",
          borderColor: "rgba(82, 205, 255, 1)",
          borderWidth: 1,
          pointStyle: "circle",
        },
      ],
    },
    options: {
      aspectRatio: 3,
      scales: {
        yAxes: [{
            gridLines: {
                display: true,
                lineWidth: 0.5  // Adjust this value as needed
            }
        }],
        xAxes: [{
            gridLines: {
                display: false
            }
        }],
      },
    },
  });
}
function createLineChartYear(datathisyear, datalastyear) {
    var ctx = document.getElementById("lineChartYear").getContext("2d");
    var lineChartMonth = new Chart(ctx, {
      type: "line",
      data: {
        labels: ["Tháng 1", "Tháng 2", "Tháng 3", "Tháng 4", "Tháng 5", "Tháng 6", "Tháng 7", "Tháng 8", "Tháng 9", "Tháng 10", "Tháng 11", "Tháng 12"],
        datasets: [
          {
            label: "Năm nay",
            data: [2, 10, 5, 2, 20, 30, 45, 50, 60, 70, 80, 90],
            backgroundColor: "rgba(83, 109, 220, 0.2)",
            borderColor: "rgba(83, 109, 220, 1)",
            pointStyle: "circle",
            borderWidth: 1,
            pointStyle: "circle",
          },
          {
            label: "Năm ngoái",
            data: [0, 5, 2, 8, 15, 25, 30, 40, 50, 60, 70, 80],
            backgroundColor: "rgba(82, 205, 255, 0.2)",
            borderColor: "rgba(82, 205, 255, 1)",
            borderWidth: 1,
            pointStyle: "circle",
          },
        ],
      },
      options: {
        aspectRatio: 3,
        scales: {
          yAxes: [{
              gridLines: {
                  display: true,
                  lineWidth: 0.5  // Adjust this value as needed
              }
          }],
          xAxes: [{
              gridLines: {
                  display: false
              }
          }],
        },
      },
    });
  }
document.addEventListener("DOMContentLoaded", function () {
  var sumIncome = document.getElementById("hp_sumIncome");
  var sumExpense = document.getElementById("hp_sumExpense");
  var sumProfit = document.getElementById("hp_sumProfit");
  var percentIncome = document.getElementById("hp_percentIncome");
  var percentExpense = document.getElementById("hp_percentExpense");
  var percentProfit = document.getElementById("hp_percentProfit");
  fetch("/get_data")
  .then((response) => response.json())
  .then((data) => {
    sumIncome.innerHTML = data.sumIncome;
    sumExpense.innerHTML = data.sumExpense;
    sumProfit.innerHTML = data.sumProfit;
    percentIncome.innerHTML = data.percentIncome;
    percentExpense.innerHTML = data.percentExpense;
    percentProfit.innerHTML = data.percentProfit;
    createLineChartMonth(data.datathismonth, data.datalastmonth);
    createLineChartYear(data.datathisyear, data.datalastyear);
  });
  createLineChartMonth();
  createLineChartYear();
});
