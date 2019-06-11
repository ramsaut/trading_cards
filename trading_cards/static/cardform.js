    window.addEventListener('DOMContentLoaded', function () {
      var avatar = document.getElementById('avatar');
      var image = document.getElementById('image');
      var input = document.getElementById('input');
      var formInput = document.getElementById('id_image');
      var $progress = $('.progress');
      var $progressBar = $('.progress-bar');
      var $alert = $('.alert');
      var $modal = $('#modal');
      var cropper;
      $('[data-toggle="tooltip"]').tooltip();
      input.addEventListener('change', function (e) {
        var files = e.target.files;
        var done = function (url) {
          input.value = '';
          image.src = url;
          $alert.hide();
          $modal.modal('show');
        };
        var reader;
        var file;
        var url;
        if (files && files.length > 0) {
          file = files[0];
          if (URL) {
            done(URL.createObjectURL(file));
          } else if (FileReader) {
            reader = new FileReader();
            reader.onload = function (e) {
              done(reader.result);
            };
            reader.readAsDataURL(file);
          }
        }
      });
      $modal.on('shown.bs.modal', function () {
        cropper = new Cropper(image, {
          aspectRatio: 795/1512,
          viewMode: 2
        });
      }).on('hidden.bs.modal', function () {
        cropper.destroy();
        cropper = null;
      });
      document.getElementById('crop').addEventListener('click', function () {
        var canvas;
        $modal.modal('hide');
        if (cropper) {
          canvas = cropper.getCroppedCanvas();
          var HERMITE = new Hermite_class();
          HERMITE.resample_single(canvas,795,1512, true);

          avatar.src = canvas.toDataURL();
          $progress.show();
          $alert.removeClass('alert-success alert-warning');
          canvas.toBlob(function (blob) {
            var done = function (url) {
             formInput.value = url;
            };
            var reader;
            reader = new FileReader();
            reader.onload = function (e) {
              done(reader.result);
            };
            reader.readAsDataURL(blob);
          });
        }
      });
      $('#id_cata').removeAttr('required');
      $('#id_cata').parent().hide();
      $('#id_catb').removeAttr('required');
      $('#id_catb').parent().hide();
      $('#id_catc').removeAttr('required');
      $('#id_catc').parent().hide();
      $('#id_catd').removeAttr('required');
      $('#id_catd').parent().hide();
      $('#id_number').parent().hide();
      $("#id_team").change(function () {
        var team = this.value;
        if(team == '25_Rare') {
            $('#id_cata').removeAttr('required');
            $('#id_cata').parent().hide();
            $('#id_catb').removeAttr('required');
            $('#id_catb').parent().hide();
            $('#id_catc').removeAttr('required');
            $('#id_catc').parent().hide();
            $('#id_catd').removeAttr('required');
            $('#id_catd').parent().hide();
        } else {
            $('#id_cata').attr('required', '');
            $('#id_cata').parent().show();
            $('#id_catb').attr('required', '');
            $('#id_catb').parent().show();
            $('#id_catc').attr('required', '');
            $('#id_catc').parent().show();
            $('#id_catd').attr('required', '');
            $('#id_catd').parent().show();
        }
        if(team == '25_Rare' || team == '24_Ref' || team == '23_Snitch' || team == '22_Volunteer' || team == '21_Committee') {
            $('#id_number').removeAttr('required');
            $('#id_number').parent().hide();
        } else {
            $('#id_number').attr('required', '');
            $('#id_number').parent().show();
        }
      });
    });