<!DOCTYPE html>
<html>
<head> 
    @include('admin.css')

    <!-- Bootstrap CSS for Modal -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css">
    
    <!-- SweetAlert2 CSS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@11/dist/sweetalert2.min.css">

    <style>
        .table_deg {
            border: 2px solid white;
            margin: auto;
            width: 100%;
            text-align: center;
            margin-top: 40px;
        }
        .th_deg {
            background-color: skyblue;
            padding: 8px;
        }
        tr {
            border: 3px solid white;
        }
        /* Custom Modal Styling */
        .modal-content {
            color:white;
        }
        .modal-header {
            background-color: #007bff; /* Blue header */
            color: white;
        }
        .modal-footer {
            background-color: #f0f8ff;
        }
        .btn-close {
            color: white;
        }
    </style>
</head>
<body>
    @include('admin.header')
    @include('admin.sidebar')

    <div class="page-content">
        <div class="page-header">
          <div class="container-fluid">
            <table class="table_deg">
                <tr>
                    <th class="th_deg">R_id</th>
                    <th class="th_deg">Customer name</th>
                    <th class="th_deg">Email</th>
                    <th class="th_deg">Phone</th>
                    <th class="th_deg">Arrival Date</th>
                    <th class="th_deg">Leaving Date</th>
                    <th class="th_deg">Status</th>
                    <th class="th_deg">Total Price</th>
                    <th class="th_deg">Report</th>
                    <th class="th_deg">Delete</th>
                    <th class="th_deg">Status Update</th>
                </tr>

                @foreach ($datas as $data)
                <tr>
                    <td>{{ $data->room_id }}</td>
                    <td>{{ $data->name }}</td>
                    <td>{{ $data->email }}</td>
                    <td>{{ $data->phone }}</td>
                    <td>{{ $data->start_date }}</td>
                    <td>{{ $data->end_date }}</td>
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
                    <td>{{ $data->total_price }}</td>
                    <td>
                        <!-- Report Button with Data -->
                        <button class="btn btn-info" onclick="showReport({{ json_encode($data) }})">Report</button>
                    </td>
                    <td>
                        <!-- Delete Button with SweetAlert2 -->
                        <button class="btn btn-danger" onclick="confirmDelete('{{ url('delete_booking', $data->id) }}')">Delete</button>
                    </td>
                    <td>
                        <a class="btn btn-success" href="{{ url('approve_book', $data->id) }}">Approved</a>
                        <a class="btn btn-warning" href="{{ url('reject_book', $data->id) }}">Rejected</a>
                    </td>
                </tr>
                @endforeach
            </table>
          </div>
        </div>
    </div>

    @include('admin.footer')

    <!-- Bootstrap JS for Modal -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>

    <!-- SweetAlert2 JS -->
    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11/dist/sweetalert2.all.min.js"></script>

    <!-- Report Modal -->
    <div class="modal fade" id="reportModal" tabindex="-1" aria-labelledby="reportModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="reportModalLabel">Booking Report</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body" id="reportContent">
                    <!-- Report details will be dynamically filled here -->
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-primary" onclick="printReport()">Print Report</button>
                </div>
            </div>
        </div>
    </div>

    <!-- JavaScript to Show Report, Print, and Handle Delete -->
    <script>
        // Function to display the report in the modal
        function showReport(data) {
            // Construct the report content
            var reportContent = `
                <p><strong>Room ID:</strong> ${data.room_id}</p>
                <p><strong>Customer Name:</strong> ${data.name}</p>
                <p><strong>Email:</strong> ${data.email}</p>
                <p><strong>Phone:</strong> ${data.phone}</p>
                <p><strong>Arrival Date:</strong> ${data.start_date}</p>
                <p><strong>Leaving Date:</strong> ${data.end_date}</p>
                <p><strong>Status:</strong> ${data.status}</p>
                <p><strong>Total Price:</strong> $${data.total_price}</p>
            `;

            // Inject the report content into the modal
            document.getElementById('reportContent').innerHTML = reportContent;

            // Show the modal
            var reportModal = new bootstrap.Modal(document.getElementById('reportModal'));
            reportModal.show();
        }

        // Function to print the report
        function printReport() {
            var content = document.getElementById('reportContent').innerHTML;
            var originalContent = document.body.innerHTML;

            document.body.innerHTML = `<html><head><title>Print Report</title></head><body>${content}</body></html>`;
            window.print();
            document.body.innerHTML = originalContent;
        }

        // Function to handle delete confirmation with SweetAlert2
        function confirmDelete(url) {
            Swal.fire({
                title: 'Are you sure?',
                text: 'You will not be able to recover this booking!',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Yes, delete it!',
                cancelButtonText: 'Cancel'
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.href = url;
                }
            });
        }
    </script>
</body>
</html>
