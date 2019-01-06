var formData = new FormData();
            formData.append('avatar', blob, 'avatar.jpg');
            $.ajax('https://jsonplaceholder.typicode.com/posts', {
              method: 'POST',
              data: formData,
              processData: false,
              contentType: false,
              xhr: function () {
                var xhr = new XMLHttpRequest();
                xhr.upload.onprogress = function (e) {
                  var percent = '0';
                  var percentage = '0%';
                  if (e.lengthComputable) {
                    percent = Math.round((e.loaded / e.total) * 100);
                    percentage = percent + '%';
                    $progressBar.width(percentage).attr('aria-valuenow', percent).text(percentage);
                  }
                };
                return xhr;
              },
              success: function () {
                $alert.show().addClass('alert-success').text('Upload success');
              },
              error: function () {
                $alert.show().addClass('alert-warning').text('Upload error');
              },
              complete: function () {
                $progress.hide();
              },
            });