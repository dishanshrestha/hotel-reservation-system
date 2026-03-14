<!DOCTYPE html>
<html lang="en">
   <head>
    <base href="/public">
      @include('home.css')
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
    
    <!-- Add Font Awesome CDN link -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    <!-- Add Bootstrap CSS link -->
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">



    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>

     <!-- SweetAlert CSS -->
     <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@11.0.18/dist/sweetalert2.min.css">
    <!-- SweetAlert JS -->
    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11.0.18/dist/sweetalert2.min.js"></script>

      <style>
        label{
            display: inline-block;
            width: 200px;
        }
        input{
            width: 100%;
        }
        
      </style>
   </head>
   <!-- body -->
   <body class="main-layout">
      <!-- loader  -->
      <div class="loader_bg">
         <div class="loader"><img src="images/loading.gif" alt="#"/></div>
      </div>
      <!-- end loader -->
      <!-- header -->
      <header>
            @include('home.header')
      </header>


      <div  class="our_room">
         <div class="container">
            <div class="row">
               <div class="col-md-12">
                  <div class="titlepage">
                     <h2>Our Room</h2>
                     <p>Our Best Service Can Impress The Customers </p>
                  </div>
               </div>
            </div>

            <div class="row">

               <div class="col-md-8">
                  <div id="serv_hover"  class="room">
                     <div style="padding:10px;" class="room_img">
                        <img style="height: 300px; width: 800px" src="/room/{{$room->image}}" alt="#"/>
                     </div>
                     <div class="bed_room">
                        <h4>{{$room->room_title}}</h4>

                        <!-- //Rating a Room -->
                                        <div class="star-rating room mt-2" title="">
                                            <div class="back-stars">
                                                <i class="fa fa-star" aria-hidden="true"></i>
                                                <i class="fa fa-star" aria-hidden="true"></i>
                                                <i class="fa fa-star" aria-hidden="true"></i>
                                                <i class="fa fa-star" aria-hidden="true"></i>
                                                <i class="fa fa-star" aria-hidden="true"></i>
                                                
                                                <div class="front-stars" style="width: {{$avgRatingPer}}%">
                                                    <i class="fa fa-star" aria-hidden="true"></i>
                                                    <i class="fa fa-star" aria-hidden="true"></i>
                                                    <i class="fa fa-star" aria-hidden="true"></i>
                                                    <i class="fa fa-star" aria-hidden="true"></i>
                                                    <i class="fa fa-star" aria-hidden="true"></i>
                                                </div>
                                            </div>
                                        <small class="pt-1">({{($room->room_ratings_count > 1)?
                                        $room->room_ratings_count.' Reviews':
                                        $room->room_ratings_count.' Review'}})</small>
                                        </div>  
                                        

                        <!-- <p style="padding: 12px">{{$room->description}}</p> -->
                        <h6 style="padding: 2px">Free Wifi : {{$room->wifi}}</h6>
                        <h6 style="padding: 2px">Room Type : {{$room->room_type}}</h6>
                        <!-- <h3 style="padding: 12px">Price : {{$room->price}}</h3> -->
                        <h6 style="padding: 2px">Price per night: <span id="pricePerNight">{{$room->price}}</span></h6>
                        <!-- <h6 style="padding: 2px">Total Price: <span id="totalPrice">0</span></h6> -->
                     </div>
                  </div>
               </div>
             

            <div class="col-md-4">
                <h1 style="font-size: 40px;">Book Room</h1>

                <div>
                    <!-- message came from HomeController -->

                    @if (session()->has('message'))
                        <div class="alert alert-success">
                        <button type="button" class="close" data-bs-dismiss="alert">X</button>
                        {{session()->get('message')}}
                        </div>
                        
                    @endif

                </div>

                @if($errors)

                @foreach($errors->all() as $errors)

                <li style="color:red">
                    {{$errors}}
                </li>

                @endforeach

                @endif

           
            <form action="{{ route('checkout') }}" method="post">
    @csrf
    <div>
        <label>Name</label>
        <input type="text" name="name" 
        @if(Auth::id())
        value="{{ Auth::user()->name }}"
        @endif
        >
    </div>
    <div>
        <label>Email</label>
        <input type="email" name="email"
        @if(Auth::id())
        value="{{ Auth::user()->email }}"
        @endif
        >
    </div>
    <div>
        <label>Phone</label>
        <input type="number" name="phone"
        @if(Auth::id())
        value="{{ Auth::user()->phone }}"
        @endif
        >
    </div>
    <div>
        <label>Start Date</label>
        <input type="date" name="startDate" id="startDate">
    </div>
    <div>
        <label>End Date</label>
        <input type="date" name="endDate" id="endDate">
    </div>
    <div>
        <label>Total Price</label>
        <input type="text" name="total_price" id="totalPriceInput" readonly>
    </div>

    <!-- Hidden input to store room ID -->
    <input type="hidden" name="room_id" value="{{ $room->id }}">

    <br>
    <div>
        @if(Auth::id())
        <button type="submit" style="background-color: #4CAF50; color: white; padding: 12px 30px; border: none; border-radius: 6px; font-weight: 600; cursor: pointer; width: 100%; font-size: 16px;" class="btn">
            <i class="fas fa-calendar-check mr-2"></i>Book Room
        </button>
        @else
        <a href="{{ route('login') }}" style="background-color: #2196F3; color: white; padding: 12px 30px; border: none; border-radius: 6px; font-weight: 600; cursor: pointer; width: 100%; text-align: center; display: block; text-decoration: none; font-size: 16px;">
            <i class="fas fa-sign-in-alt mr-2"></i>Login to Book
        </a>
        @endif
    </div>
</form>

            </div>
            
            <div class="col-md-12">
                <ul class="nav nav-tabs" id="myTab" role="tablist">
                    <li class="nav-item" role="presentation">
                        <button class="nav-link active" id="description-tab" data-bs-toggle="tab" data-bs-target="#description" role="tab" aria-controls="description" aria-selected="true">Description</button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link" id="reviews-tab" data-bs-toggle="tab" data-bs-target="#reviews" role="tab" aria-controls="reviews" aria-selected="false">Reviews</button>
                    </li>
                </ul>
                <div class="tab-content" id="myTabContent">
                    <div class="tab-pane fade show active" id="description" role="tabpanel" aria-labelledby="description-tab">
                        {!! $room->description !!}
                    </div>
                    <div class="tab-pane fade" id="reviews" role="tabpanel" aria-labelledby="reviews-tab">
                            <div class="col-md-8">
                            <div class="row">
                        <form action="" name="roomRatingForm" id="roomRatingForm" method="post">
                            @csrf
                            <h3 class="h4 pb-3">Write a Review</h3>
                            <div class="form-group col-md-6 mb-3">
                                <label for="name">Name</label>
                                <input type="text" class="form-control" name="name" id="name" placeholder="Name">
                                <p></p>
                            </div>
                            <div class="form-group col-md-6 mb-3">
                                <label for="email">Email</label>
                                <input type="text" class="form-control" name="email" id="email" placeholder="Email">
                                <p></p>
                            </div>
                            <div class="form-group mb-3">
                                <label for="rating">Rating</label>
                                <br>
                                <div class="rating" style="width: 10rem">
                                    <input id="rating-5" type="radio" name="rating" value="5"/><label for="rating-5"><i class="fas fa-3x fa-star"></i></label>
                                    <input id="rating-4" type="radio" name="rating" value="4"/><label for="rating-4"><i class="fas fa-3x fa-star"></i></label>
                                    <input id="rating-3" type="radio" name="rating" value="3"/><label for="rating-3"><i class="fas fa-3x fa-star"></i></label>
                                    <input id="rating-2" type="radio" name="rating" value="2"/><label for="rating-2"><i class="fas fa-3x fa-star"></i></label>
                                    <input id="rating-1" type="radio" name="rating" value="1"/><label for="rating-1"><i class="fas fa-3x fa-star"></i></label>
                                </div>
                                <p class="room-rating-error text-danger"></p>
                            </div>
                            <div class="form-group mb-3">
                                <label for="comment">How was your Experience?</label>
                                <textarea name="comment" id="comment" class="form-control" cols="30" rows="10" placeholder="How was your overall experience?"></textarea>
                                <p></p>
                            </div>
                            <div>
                                <button class="btn btn-dark" type="submit">Submit</button>
                            </div>
                        </form>

                                    
                                </div>
                            </div>
                            <div class="col-md-12 mt-5">
                                <div class="overall-rating mb-3">
                                    <div class="d-flex">
                                        <h1 class="h3 pe-3 mt-3">{{$avgRating}}</h1>
                                        <div class="star-rating mt-2" title="">
                                            <div class="back-stars">
                                                <i class="fa fa-star" aria-hidden="true"></i>
                                                <i class="fa fa-star" aria-hidden="true"></i>
                                                <i class="fa fa-star" aria-hidden="true"></i>
                                                <i class="fa fa-star" aria-hidden="true"></i>
                                                <i class="fa fa-star" aria-hidden="true"></i>
                                                
                                                <div class="front-stars" style="width: {{$avgRatingPer}}%">
                                                    <i class="fa fa-star" aria-hidden="true"></i>
                                                    <i class="fa fa-star" aria-hidden="true"></i>
                                                    <i class="fa fa-star" aria-hidden="true"></i>
                                                    <i class="fa fa-star" aria-hidden="true"></i>
                                                    <i class="fa fa-star" aria-hidden="true"></i>
                                                </div>
                                            </div>
                                        </div>  
                                        <div class="pt-2 ps-2 mt-3">({{($room->room_ratings_count > 1)?
                                        $room->room_ratings_count.' Reviews':
                                        $room->room_ratings_count.' Review'}})</div>
                                    </div>
                                    
                                </div>
                                
                            @if($room->room_ratings->isNotEmpty())
                                @foreach ($room->room_ratings as $rating)
                                    @php
                                    $ratingPer = ($rating->rating / 5) * 100;
                                    @endphp

                                    <div class="rating-group mb-4">
                                        <span class="author"><strong>{{ $rating->username }} </strong></span>
                                        <div class="star-rating mt-2" title="Rating: {{ $rating->rating }} out of 5">
                                            <div class="back-stars">
                                                <i class="fa fa-star" aria-hidden="true"></i>
                                                <i class="fa fa-star" aria-hidden="true"></i>
                                                <i class="fa fa-star" aria-hidden="true"></i>
                                                <i class="fa fa-star" aria-hidden="true"></i>
                                                <i class="fa fa-star" aria-hidden="true"></i>
                                                
                                                <div class="front-stars" style="width: {{ $ratingPer }}%;">
                                                    <i class="fa fa-star" aria-hidden="true"></i>
                                                    <i class="fa fa-star" aria-hidden="true"></i>
                                                    <i class="fa fa-star" aria-hidden="true"></i>
                                                    <i class="fa fa-star" aria-hidden="true"></i>
                                                    <i class="fa fa-star" aria-hidden="true"></i>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="my-3">
                                            <p>{{ $rating->comment }}</p>
                                        </div>
                                    </div>
                                @endforeach
                            @endif

                            </div>
                        </div>
                </div>
            </div>


         </div>
      </div>


     
      <!--  footer -->
            @include('home.footer')

            <script>
                $(function(){
                    var dtToday = new Date();
                    var month = dtToday.getMonth() + 1;  //dtToday.getMonth() + 1 gets the current month (0-11) and adds 1 to make it 1-12.
                    var day = dtToday.getDate();
                    var year = dtToday.getFullYear();
                    //If the month or day is less than 10, add a leading zero to ensure a two-digit format (e.g., 1 becomes 01)
                    if(month < 10)
                        month = '0' + month.toString();

                    if(day < 10)
                    day = '0' + day.toString();
                    var maxDate = year + '-' + month + '-' + day; //Concatenate the year, month, and day to create a string in the format YYYY-MM-DD.
                    $('#startDate').attr('min',maxDate);
                    $('#endDate').attr('min',maxDate);

                
                function calculateTotalPrice() {
                    var startDate = new Date($('#startDate').val());
                    var endDate = new Date($('#endDate').val());

                    if (startDate && endDate && endDate > startDate) {
                        var timeDifference = endDate.getTime() - startDate.getTime();
                        var nights = timeDifference / (1000 * 3600 * 24);
                        
                        var pricePerNight = parseFloat($('#pricePerNight').text());
                        var totalPrice = nights * pricePerNight;

                        $('#totalPriceInput').val(totalPrice.toFixed(1));
                    } else {
                        $('#totalPriceInput').val('0');
                    }
                }

                $('#startDate, #endDate').on('change', calculateTotalPrice);

        });
    </script>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.min.js" integrity="sha384-BBtl+eGJRgqQAUMxJ7pMwbEyER4l1g+O15P+16Ep7Q9Q+zqX6gSbd85u4mG4QzX+" crossorigin="anonymous"></script>

        <script>
            $(document).ready(function(){
                $("#roomRatingForm").submit(function(event){
                    event.preventDefault();

                    $.ajax({
                        url: '{{ route("front.saveRating", $room->id) }}',
                        type: 'post',
                        data: $(this).serializeArray(),
                        dataType: 'json',
                        headers: {
                            'X-CSRF-TOKEN': '{{ csrf_token() }}'
                        },
                        success: function(response){
                            console.log(response);  // Added for debugging

                            if (response.status == 'duplicate') {
                                Swal.fire({
                                    icon: 'error',
                                    title: 'Duplicate Rating',
                                    text: response.message
                                });
                                return;
                            }

                            var errors = response.errors;

                            if(response.status == false){
                                if(errors.name){
                                    $("#name").addClass('is-invalid')
                                    .siblings("p")
                                    .addClass('invalid-feedback')
                                    .html(errors.name);
                                } else {
                                    $("#name").removeClass('is-invalid')
                                    .siblings("p")
                                    .removeClass('invalid-feedback')
                                    .html('');  // Clear previous errors
                                }

                                if(errors.email){
                                    $("#email").addClass('is-invalid')
                                    .siblings("p")
                                    .addClass('invalid-feedback')
                                    .html(errors.email);
                                } else {
                                    $("#email").removeClass('is-invalid')
                                    .siblings("p")
                                    .removeClass('invalid-feedback')
                                    .html('');  // Clear previous errors
                                }

                                if(errors.comment){
                                    $("#comment").addClass('is-invalid')
                                    .siblings("p")
                                    .addClass('invalid-feedback')
                                    .html(errors.comment);
                                } else {
                                    $("#comment").removeClass('is-invalid')
                                    .siblings("p")
                                    .removeClass('invalid-feedback')
                                    .html('');  // Clear previous errors
                                }

                                if(errors.rating){
                                    $(".room-rating-error").html(errors.rating);
                                } else {
                                    $(".room-rating-error").html('');  // Clear previous errors
                                }
                            } else {
                                Swal.fire({
                                    icon: 'success',
                                    title: 'Review Submitted',
                                    text: 'Thanks for Rating!'
                                });
                            }
                        },
                        error: function(xhr, status, error){
                            console.log(xhr.responseText);  // Added for debugging
                        }
                    });
                });
            });
        </script>


   </body>
</html>