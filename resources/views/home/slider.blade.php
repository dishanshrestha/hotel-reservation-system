<section class="banner_main">
    <div id="myCarousel" class="carousel slide banner" data-ride="carousel">
        <ol class="carousel-indicators">
            <li data-target="#myCarousel" data-slide-to="0" class="active"></li>
            <li data-target="#myCarousel" data-slide-to="1"></li>
            <li data-target="#myCarousel" data-slide-to="2"></li>
        </ol>
        <div class="carousel-inner">
            <div class="carousel-item active">
                <img class="first-slide" src="images/banner1.jpg" alt="First slide">
                <div class="container">
                </div>
            </div>
            <div class="carousel-item">
                <img class="second-slide" src="images/banner2.jpg" alt="Second slide">
            </div>
            <div class="carousel-item">
                <img class="third-slide" src="images/banner3.jpg" alt="Third slide">
            </div>
        </div>
        <a class="carousel-control-prev" href="#myCarousel" role="button" data-slide="prev">
            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
            <span class="sr-only">Previous</span>
        </a>
        <a class="carousel-control-next" href="#myCarousel" role="button" data-slide="next">
            <span class="carousel-control-next-icon" aria-hidden="true"></span>
            <span class="sr-only">Next</span>
        </a>
    </div>


    <div class="booking_ocline">
        <div class="container">
            <div class="row">
                <div class="col-md-5">
                    <div class="book_room">
                        <h1>Search for Rooms</h1>
                        <form class="book_now" action="{{ route('search.rooms') }}" method="GET">
                            <div class="row">
                                <div class="col-md-12">
                                    <span>Price Range</span>
                                    <select class="online_book" name="price_range" style="background-color: #000000c7;">
                                        <option value="">Select Price Range</option>
                                        <option value="0-1000">0 - 1000</option>
                                        <option value="1000-5000">1000 - 5000</option>
                                        <option value="5000-10000">5000 - 10000</option>
                                        <option value="10000-20000">10000 - 20000</option>
                                    </select>
                                </div>
                                <div class="col-md-12">
                                    <span>Room Type</span>
                                    <select class="online_book" name="room_type" style="background-color: #000000c7;">
                                        <option selected value="regular">Regular</option>
                                        <option value="premium">Premium</option>
                                        <option value="deluxe">Deluxe</option>
                                        <option value="single">Single</option>
                                        <option value="double">Double</option>
                                    </select>
                                </div>
                                <div class="col-md-12">
                                    <button class="book_btn" type="submit">Search</button>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>

</section>