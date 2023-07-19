$(document).ready(function() {
    $('table.sortable th a').click(function(e) {
      e.preventDefault();
      var url = $(this).attr('href');
      var tbody = $(this).closest('table').find('tbody');
  
      $.ajax({
        url: url,
        success: function(data) {
          var rows = $(data).find('tbody tr');
          tbody.empty();
          rows.each(function() {
            tbody.append($(this));
          });
        }
      });
    });
  
    $('input[name="table_search"]').keyup(function() {
      var searchText = $(this).val().toLowerCase();
      var table = $(this).closest('.card').find('table');
      var rows = table.find('tbody tr');
  
      rows.each(function() {
        var rowText = $(this).text().toLowerCase();
        if (rowText.indexOf(searchText) === -1) {
          $(this).hide();
        } else {
          $(this).show();
        }
      });
    });



  });

  function submitForm() {
    document.getElementById('update-form').submit();
}
// document.addEventListener("DOMContentLoaded", function() {
    function createData() {
      var table = document.getElementById('myTable');
      var form = document.getElementById('form');
      var test = document.getElementById('test')

      console.log('thios is the test '+form)
      var value = form.value;
        console.log(value);
      var data = [];
    
      if (!table || !form) {
        console.error("Table or form element not found.");
        return;
      }
      
      var headers = [];
      var tableHeaderRow = table.querySelector('thead tr');
      if (!tableHeaderRow) {
        console.error("Table header row not found.");
        return;
      }
      
      for (var i = 0; i < tableHeaderRow.cells.length; i++) {
        headers.push(tableHeaderRow.cells[i].innerText);
      }
      
      var tableDataRows = table.querySelectorAll('tbody tr');
      if (!tableDataRows.length) {
        console.error("Table data rows not found.");
        return;
      }
      
      for (var i = 0; i < tableDataRows.length; i++) {
        var rowData = {};
        var dataRow = tableDataRows[i];
        
        for (var j = 0; j < headers.length; j++) {
          rowData[headers[j]] = dataRow.cells[j].innerText;
        }
        
        data.push(rowData);
      }
    
      var formData = new FormData(form);
      var formObject = {};
      for (var [key, value] of formData.entries()) {
        formObject[key] = value;
      }
      
      data.push(formObject);
    
      console.log(data);
    }
//   });


function formatDate() {
  var currentDate = new Date();
  var daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  var months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

  var day = daysOfWeek[currentDate.getDay()];
  var date = currentDate.getDate();
  var month = months[currentDate.getMonth()];
  var year = currentDate.getFullYear();

  // Add appropriate suffix to the date
  var suffix = getNumberSuffix(date);
  var formattedDate = day + ' ' + date + suffix + ' ' + month + ', ' + year;

  document.getElementById('current-date').textContent = formattedDate;
}

function getNumberSuffix(date) {
  if (date >= 11 && date <= 13) {
    return 'th';
  } else {
    var lastDigit = date % 10;
    switch (lastDigit) {
      case 1:
        return 'st';
      case 2:
        return 'nd';
      case 3:
        return 'rd';
      default:
        return 'th';
    }
  }
}

// Call the formatDate function when the page loads
window.addEventListener('DOMContentLoaded', formatDate);