<div  class="gallery">
         <div class="container">
            <div class="row">
               <div class="col-md-12">
                  <div class="titlepage">
                     <h2>gallery</h2>
                  </div>
               </div>
            </div>
            <div class="row">

            @foreach ($gallery as $gallary)
               @php
                  $src = $gallary->image;
                  if (!\Illuminate\Support\Str::startsWith($src, ['http://','https://'])) {
                      $src = url('/gallary/'.$src);
                  }
               @endphp

               <div class="col-md-3 col-sm-6">
                  <div class="gallery_img">
                     <figure><img src="{{ $src }}" alt="#"/></figure>
                  </div>
               </div>

            @endforeach
            </div>
         </div>
      </div>