<!DOCTYPE html>
<html lang="en">

<head>
    @include('home.css')
    <style>
        .table_deg {
            border: 2px solid white;
            margin: auto;
            width: 100%;
            text-align: center;
            margin-top: 40px;
            color: #fff;
        }

        .th_deg {
            background-color: #0f1521;
            padding: 8px;
        }

        tr {
            border: 3px solid white;
        }

        td {
            padding: 3px;
            color: #000;
        }
    </style>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"
        integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.min.js"
        integrity="sha384-BBtl+eGJRgqQAUMxJ7pMwbEyER4l1g+O15P+16Ep7Q9Q+zqX6gSbd85u4mG4QzX+"
        crossorigin="anonymous"></script>

</head>
<!-- body -->

<body class="main-layout">
    <!-- loader  -->
    <div class="loader_bg">
        <div class="loader"><img src="images/loading.gif" alt="#" /></div>
    </div>
    <!-- end loader -->
    <!-- header -->
    <header>
        @include('home.header')
    </header>
    <!-- end header inner -->

    <div>

        <table class="table_deg">
            <h1 style="color: #0f1521; text-align: center; font-size: 30px; font-weight: bold;margin-top:10px">My
                Booking Details</h1>
            <tr>
                <th class="th_deg">Customer name</th>
                <th class="th_deg">Arrival Date</th>
                <th class="th_deg">Leaving Date</th>
                <th class="th_deg">Status</th>
                <th class="th_deg">Room Title</th>
                <th class="th_deg">Total Price</th>
                <th class="th_deg">Image</th>
                <th class="th_deg">Status Update</th>


            </tr>
            @foreach ($datas as $data)
                <tr>
                    <td>{{$data->name}}</td>
                    <td>{{$data->start_date}}</td>
                    <td>{{$data->end_date}}</td>
                    <td>
                        @if ($data->status == 'paid')
                            <span style="color:green;">Approved</span>
                        @endif
                        @if ($data->status == 'rejected')
                            <span style="color:red;">Rejected</span>
                        @endif
                        @if ($data->status == 'canceled')
                            <span style="color:red;">Cancelled</span>
                        @endif
                        @if ($data->status == 'waiting')
                            <span style="color:yellow;">Waiting</span>
                        @endif
                    </td>
                    <td>{{$data->room->room_title}}</td>
                    <td>{{$data->total_price}}</td>
                    <td>
                        <img style="width:150px; height: 80px;" src="/room/{{$data->room->image}}" alt="">
                    </td>
                    <td>
                        <span style="padding-bottom: 5px ">

                            <a class="btn btn-danger" href="{{url('cancel_book', $data->id)}}">Cancel</a>

                        </span>
                    </td>
                </tr>
            @endforeach
        </table>
    </div>

    <!--  footer -->
    @include('home.footer')

</body>

</html>