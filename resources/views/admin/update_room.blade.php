<!DOCTYPE html>
<html>
  <head> 
  <base href="/public"><!-- saying that all css is in public folder -->
    @include('admin.css')
    <style type="text/css">

        label{
            display: inline-block;
            width: 200px;
        }

        .div_deg{
            padding-top: 30px;
        }

        .div_center{
            margin-left: 20px;
            padding-top:40px;
        }

    </style>
  </head>
  <body>
    @include('admin.header')
    
    @include('admin.sidebar')
     
    <div class="page-content">
        <div class="page-header">
          <div class="container-fluid">

                <div class="div_center">
                    <h1 style="font-size: 30px; font-weight: bold;">Update Room</h1>

                    <form action="{{url('edit_room',$data->id)}}" method="Post" enctype="multipart/form-data">
                       
                         <!-- //Cross-Site Request Forgery -->
                         @csrf   
                        <div class="div_deg">
                            <label>Room Title</label>
                            <input type="text" name="title" value="{{$data->room_title}}">
                        </div>

                        <div class="div_deg">
                            <label>Description</label>
                           <textarea name="description">{{$data->description}}</textarea>
                        </div>

                        <div class="div_deg">
                            <label>Price</label>
                            <input type="number" name="price" value="{{$data->price}}">
                        </div>

                        <div class="div_deg">
                            <label>Room Type</label>
                          <select name="type" id="">
                            <option selected value="{{$data->room_type}}">{{$data->room_type}}</option>
                                <option value="regular">Regular</option>
                                <option value="premium">Premium</option>
                                <option value="deluxe">Deluxe</option>
                                <option value="single">Single</option>
                                <option value="double">Double</option>

                          </select>
                        </div>

                        <div class="div_deg">
                            <label>Free Wifi</label>
                          <select name="wifi" id="">
                          <option selected value="value="{{$data->wifi}}"">{{$data->wifi}}</option>
                                <option selected value="yes">Yes</option>
                                <option value="no">No</option>
                          </select>
                        </div>

                        <div class="div_deg">
                            <label>Current Image</label>
                            <img width="100" src="/room/{{$data->image}}" alt="current image">
                        </div>

                        <div class="div_deg">
                            <label>Upload Image</label>
                            <input type="file" name="image">
                        </div>
                        
                        <div class="div_deg">
                            <input class="btn btn-primary" type="submit" value="Update Room">
                        </div>

                    </form>
                </div>

          </div>
        </div>
    </div>
    
    @include('admin.footer')
  </body>
</html>