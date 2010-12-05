#(let* ((filelist (cadr (file-glob "*.png" 1))))
#(while (not (null? filelist))
#   ( let* ( (filename (car filelist))
#            (image (car (gimp-file-load RUN-NONINTERACTIVE filename filename)))
#     )
#     (let ( (drawable (car (gimp-image-get-active-layer image))) )
#       (let ( ( indexed (car (gimp-drawable-is-indexed drawable))))
#            (when (= 0 indexed)
#                (gimp-image-convert-indexed image 0 0 255 TRUE FALSE "")
#            )
#       )
#       (file-png-save RUN-NONINTERACTIVE image drawable filename filename 0 9 0 0 0 0 0)
#       (gimp-image-delete image)
#     )
#   )
#   (set! filelist (cdr filelist))
#)
#)


gimp_script = '(let* ((filelist (cadr (file-glob "*.png" 1)))) (while (not (null? filelist)) ( let* ( (filename (car filelist)) (image (car (gimp-file-load RUN-NONINTERACTIVE filename filename))) ) (let ( (drawable (car (gimp-image-get-active-layer image))) ) (let ( ( indexed (car (gimp-drawable-is-indexed drawable)))) (when (= 0 indexed) (gimp-image-convert-indexed image 0 0 255 TRUE FALSE "") ) ) (file-png-save RUN-NONINTERACTIVE image drawable filename filename 0 9 0 0 0 0 0) (gimp-image-delete image) ) ) (set! filelist (cdr filelist)) ) )'
command = ["gimp", "-i", "-b", gimp_script, "-b", '(gimp-quit 0)']

import subprocess

sp = subprocess.Popen(command)
sp.wait()

