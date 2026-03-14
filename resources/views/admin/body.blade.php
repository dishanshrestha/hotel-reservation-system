<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Bar Chart</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.3/dist/chart.umd.min.js"></script>
</head>
<body>

<div class="page-content">
    <div class="page-header">
        <div class="container-fluid">
            <h2 class="h5 no-margin-bottom">Dashboard</h2>
        </div>
    </div>
    <section class="no-padding-top no-padding-bottom">
        <div class="container-fluid">
            <div class="row">
                <div class="col-md-3 col-sm-6">
                    <div class="statistic-block block">
                        <div class="progress-details d-flex align-items-end justify-content-between">
                            <div class="title">
                                <div class="icon"><i class="fas fa-user"></i></div><strong>User</strong>
                            </div>
                            <div class="number dashtext-1">{{ $totalUsers }}</div>
                        </div>
                    </div>
                </div>
                <div class="col-md-3 col-sm-6">
                    <div class="statistic-block block">
                        <div class="progress-details d-flex align-items-end justify-content-between">
                            <div class="title">
                                <div class="icon"><i class="fas fa-check-circle"></i></div><strong>Booked</strong>
                            </div>
                            <div class="number dashtext-2">{{$totalBookings}}</div>
                        </div>
                    </div>
                </div>
                <div class="col-md-3 col-sm-6">
                    <div class="statistic-block block">
                        <div class="progress-details d-flex align-items-end justify-content-between">
                            <div class="title">
                                <div class="icon"><i class="fas fa-bed"></i></div><strong>Rooms</strong>
                            </div>
                            <div class="number dashtext-3">{{$totalRoom}}</div>
                        </div>
                    </div>
                </div>
                <div class="col-md-3 col-sm-6">
                    <div class="statistic-block block">
                        <div class="progress-details d-flex align-items-end justify-content-between">
                            <div class="title">
                                <div class="icon"><i class="fas fa-dollar-sign"></i></div><strong>Incomes</strong>
                            </div>
                            <div class="number dashtext-4" style="font-size: 1em;">{{$totalIncome}}</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <section class="no-padding-bottom">
        <div class="container-fluid">
            <div class="row">
                <div class="col-lg-8">
                    <div class="bar-chart block no-margin-bottom" style="height: 400px;">
                        <canvas id="chart" style="height: 325px;margin:auto;"></canvas>
                    </div>
                </div>
                <div class="col-lg-4">
                    <div class="stats-with-chart-2 block" style="height: 400px;">
                        <div class="title"><strong class="d-block">Booked</strong><span class="d-block">Thank's for Booking</span></div>
                        <div class="piechart chart">
                            <canvas id="pieChartHome1"></canvas>
                            <div class="text"><strong class="d-block">{{$approvedCount}}</strong></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <section>
        <div class="container-fluid">
            <div class="row">
                <div class="col-lg-4">
                    <div class="stats-with-chart-2 block">
                        <div class="title"><strong class="d-block">Pending</strong><span class="d-block">Ready to Pay</span></div>
                        <div class="piechart chart">
                            <canvas id="pieChartHome2"></canvas>
                            <div class="text"><strong class="d-block">{{$waitingCount}}</strong></div>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4">
                    <div class="stats-with-chart-2 block">
                        <div class="title"><strong class="d-block">Canceled</strong><span class="d-block">Don't do that</span></div>
                        <div class="piechart chart">
                            <canvas id="pieChartHome3"></canvas>
                            <div class="text"><strong class="d-block">{{$canceledCount}}</strong></div>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4">
                    <div class="stats-with-chart-2 block">
                        <div class="title"><strong class="d-block">Booking Rejected</strong><span class="d-block">Sorry Room not Available</span></div>
                        <div class="piechart chart">
                            <canvas id="pieChartHome4"></canvas> <!-- Changed ID here -->
                            <div class="text"><strong class="d-block">{{$rejectedCount}}</strong></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <script>
        // Bar chart for bookings
        var ctx = document.getElementById('chart').getContext('2d');
        var bookingChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: {!! json_encode($labels) !!},
                datasets: {!! json_encode($datasets) !!}
            },
        });

        // Pie charts for status
        var pieCtx1 = document.getElementById('pieChartHome1').getContext('2d');
        var pieChart1 = new Chart(pieCtx1, {
            type: 'pie',
            data: {
                labels: ['Approved'],
                datasets: [{
                    data: [{{$approvedCount}}],
                    backgroundColor: ['#36A2EB'],
                }]
            }
        });

        var pieCtx2 = document.getElementById('pieChartHome2').getContext('2d');
        var pieChart2 = new Chart(pieCtx2, {
            type: 'pie',
            data: {
                labels: ['Waiting'],
                datasets: [{
                    data: [{{$waitingCount}}],
                    backgroundColor: ['#FF6384'],
                }]
            }
        });

        var pieCtx3 = document.getElementById('pieChartHome3').getContext('2d');
        var pieChart3 = new Chart(pieCtx3, {
            type: 'pie',
            data: {
                labels: ['Canceled'],
                datasets: [{
                    data: [{{$canceledCount}}],
                    backgroundColor: ['#FFCE56'],
                }]
            }
        });

        var pieCtx4 = document.getElementById('pieChartHome4').getContext('2d'); // New ID for the fourth pie chart
        var pieChart4 = new Chart(pieCtx4, {
            type: 'pie',
            data: {
                labels: ['Rejected'],
                datasets: [{
                    data: [{{$rejectedCount}}],
                    backgroundColor: ['#8BC34A'],
                }]
            }
        });
    </script>

</div>
</body>
</html>
