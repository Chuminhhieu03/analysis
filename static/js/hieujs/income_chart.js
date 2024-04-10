document.addEventListener("DOMContentLoaded", function () {
  var datepicker = document.querySelector("#datepicker-income");
  $(datepicker).datepicker({
    format: "mm/yyyy",
    viewMode: "months",
    minViewMode: "months",
  });
  const userType = document.getElementById("income_user_type").value;
  var labelSource = [];
  if (userType === "0") {
    labelSource = ["Lương", "Kinh Doanh", "Phụ thu nhập", "Khác"];
  } else {
    labelSource = ["Sản phẩm", "Dịch vụ", "Quảng cáo", "Khác"];
  }
  const backgroundColorSource = ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0"];
  const borderColorSource = ["#FF6383", "#36A1EB", "#FFCE55", "#4BC0C9"];
  var dataSource = [];
  var formSource = document.getElementById("income_chart_form");
  var btn = document.getElementById("income_chart_button");
  var ctx = document.getElementById("incomeChart").getContext("2d");

  var salary_progress = document.getElementById("salary_progress");
  var business_progress = document.getElementById("business_progress");
  var other_progress = document.getElementById("other_progress");
  var submoney_progress = document.getElementById("submoney_progress");

  var salary_amount = document.getElementById("salary_amount");
  var business_amount = document.getElementById("business_amount");
  var other_amount = document.getElementById("other_amount");
  var submoney_amount = document.getElementById("submoney_amount");

  var myChart = new Chart(ctx, {
    type: "pie",
    data: {
      labels: labelSource.slice(0, 4),
      datasets: [
        {
          label: "Thu nhập",
          data: [0, 0, 0, 0],
          backgroundColor: backgroundColorSource.slice(0, 4),
          borderColor: borderColorSource.slice(0, 4),
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      animation: {
        animateScale: true,
        animateRotate: true,
      },
    },
  });

  btn.addEventListener("click", function (e) {
    fetch("/income/get_chart_data", {
      method: "POST",
      body: JSON.stringify({
        date: formSource.date.value,
      }),
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": formSource.csrfmiddlewaretoken.value,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        dataSource = data;
        const lengthData = dataSource.length;
        myChart.data.labels = labelSource.slice(0, lengthData);
        myChart.data.datasets[0].data = dataSource;
        myChart.data.datasets[0].backgroundColor = backgroundColorSource.slice(
          0,
          lengthData
        );
        myChart.data.datasets[0].borderColor = borderColorSource.slice(
          0,
          lengthData
        );
        myChart.update();
        // convert String to Number
        dataSource = dataSource.map((item) => parseInt(item));
        sumData = dataSource[0] + dataSource[1] + dataSource[2] + dataSource[3];
        salary_progress.style.width = `${(dataSource[0] / sumData) * 100}%`;
        business_progress.style.width = `${(dataSource[1] / sumData) * 100}%`;
        other_progress.style.width = `${(dataSource[2] / sumData) * 100}%`;
        submoney_progress.style.width = `${(dataSource[3] / sumData) * 100}%`;
        salary_amount.innerHTML = `${dataSource[0].toLocaleString()} VND`;
        business_amount.innerHTML = `${dataSource[1].toLocaleString()} VND`;
        other_amount.innerHTML = `${dataSource[2].toLocaleString()} VND`;
        submoney_amount.innerHTML = `${dataSource[3].toLocaleString()} VND`;
      })
      .catch((error) => {
        location.reload();
      });
  });
});
