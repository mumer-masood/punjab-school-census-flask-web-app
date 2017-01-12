(function($, window) {

    var backSpaceKey = 8;
    var startOfQualifiedKeys = 31;
    var csrf_token = $("#csrf_token").val();

    // var get_schools = function(){};

    // $("input#district_name").keyup(function (e) {
    //     if (e.keyCode === backSpaceKey || e.keyCode > startOfQualifiedKeys) {
    //         getSchools(data);
    //     }});
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
	    beforeSend: function(xhr, settings) {
	        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
	            xhr.setRequestHeader("X-CSRFToken", csrf_token);
	        }
	    }
	});

    // $("input#districts").onChange(function (e) {
    //         getSchools(data);
    // });

    // var drawStachedChart = function () {
    //     google.charts.load('current', {packages: ['corechart', 'bar']});
    //     google.charts.setOnLoadCallback(drawStacked);
    //
    //     function drawStacked() {
    //         var data = google.visualization.arrayToDataTable([
    //             ['City', '2010 Population', '2000 Population'],
    //             ['New York City, NY', 8175000, 8008000],
    //             ['Los Angeles, CA', 3792000, 3694000],
    //             ['Chicago, IL', 2695000, 2896000],
    //             ['Houston, TX', 2099000, 1953000],
    //             ['Philadelphia, PA', 1526000, 1517000]
    //         ]);
    //
    //         var options = {
    //             title: 'Population of Largest U.S. Cities',
    //             isStacked: true,
    //             hAxis: {
    //                 title: 'Total Population',
    //                 minValue: 0,
    //             },
    //             vAxis: {
    //                 title: 'City'
    //             }
    //         };
    //         var chart = new google.visualization.BarChart(
    //             document.getElementById('chart_div'));
    //         chart.draw(data, options);
    //     }
    // };

    var drawStachedChart = function (data) {
        google.charts.load("current", {packages:["corechart"]});
        google.charts.setOnLoadCallback(drawChart);
          function drawChart() {
            var data = google.visualization.arrayToDataTable([
              ['Task', 'Hours per Day'],
              data
            ]);

            var options = {
              title: 'Percentage Chart',
              is3D: true,
            };

            var chart = new google.visualization.PieChart(
                document.getElementById('chart_div'));
            chart.draw(data, options);
          }
    };
    // Get all the records to show in the package page.
    // function getSchools(page) {
    //     if (typeof(page) == "undefined") {
    //         page = 1;
    //     }
    //     $("#packagelist").mask_div("Loading...");
    //     $.ajax({
    //         type: "POST",
    //         url: "/schools/",
    //         dataType: 'json',
    //         data: {
    //             package_name: $("#package_name").val(),
    //             page: page
    //         },
    //         success: function (data) {
    //             $(".body-holder").empty();
    //             $(".body-holder").append(data);
    //             $("#packagelist").unmask_div();
    //
    //         },
    //         error: function () {
    //             $("#packagelist").unmask_div();
    //             $('<div class="error">Retrieving data failed</div>').appendTo($('#messages'));
    //             setTimeout('$(".error").remove()', 3000);
    //         }
    //     });

}).call(this, jQuery, window);
