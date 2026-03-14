<!DOCTYPE html>
<html>
  <head> 
    @include('admin.css')
  </head>
  <body>
    @include('admin.header')
    
    @include('admin.sidebar')
     
    <div class="page-content">
        <div class="page-header">
          <div class="container-fluid">
            <center>
            <h1 style="font-size: 40px;font-weight:bolder;color:white;">Gallery</h1>

            <div class="row">
                @foreach ($gallery as $gallary)
                <div class="col-md-4">
                    <img src="/gallary/{{$gallary->image}}"  style="height: 200px; width: 300px;">                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
                    <a href="{{url('delete_gallary',$gallary->id)}}" class="btn btn-danger">Delete Image</a>
                </div>
                
            
                @endforeach
            </div>

            <form action="{{url('upload_gallary')}}" method="post" enctype="multipart/form-data">
                @csrf
                <div style="padding:30px;">
                    <label style="color:white;font-weight:bold;">Upload Image</label>
                    <input type="file" name="image" required>

                    <input type="submit" value="Add Image" class="btn btn-primary">
                </div>
            </form>
            </center>

          </div>
        </div>
    </div>
    
    @include('admin.footer')
  </body>
</html>