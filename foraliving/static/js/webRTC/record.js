/*
 *  Copyright (c) 2015 The WebRTC project authors. All Rights Reserved.
 *
 *  Use of this source code is governed by a BSD-style license
 *  that can be found in the LICENSE file in the root of the source
 *  tree.
 */

'use strict';

/* globals MediaRecorder */

// This code is adapted from
// https://rawgit.com/Miguelao/demos/master/mediarecorder.html

'use strict';

/* globals MediaRecorder */

var mediaSource = new MediaSource();
mediaSource.addEventListener('sourceopen', handleSourceOpen, false);
var mediaRecorder;
var recordedBlobs;
var sourceBuffer;

var gumVideo = document.querySelector('video#gum');
// var recordedVideo = document.querySelector('video#recorded');

var recordButton = document.querySelector('button#record');
// var playButton = document.querySelector('button#play');
var downloadButton = document.querySelector('button#download');
recordButton.onclick = toggleRecording;
// playButton.onclick = play;
downloadButton.onclick = download;

// window.isSecureContext could be used for Chrome
var isSecureOrigin = location.protocol === 'https:' ||
    location.hostname === 'localhost';
if (!isSecureOrigin) {
    alert('getUserMedia() must be run from a secure origin: HTTPS or localhost.' +
        '\n\nChanging protocol to HTTPS');
    location.protocol = 'HTTPS';
}

// Use old-style gUM to avoid requirement to enable the
// Enable experimental Web Platform features flag in Chrome 49

var constraints = {
    audio: true,
    video: true
};

// navigator.getUserMedia = navigator.getUserMedia ||
//                          navigator.webkitGetUserMedia ||
//                          navigator.mozGetUserMedia;
//
// if (navigator.getUserMedia) {
//    navigator.getUserMedia({ audio: true, video: { width: 1280, height: 720 } },
//       function(stream) {
//          var video = document.querySelector('video');
//          video.src = window.URL.createObjectURL(stream);
//          video.onloadedmetadata = function(e) {
//            video.play();
//          };
//       },
//       function(err) {
//          console.log("The following error occurred: " + err.name);
//       }
//    );
// } else {
//    console.log("getUserMedia not supported");
// }

function handleSuccess(stream) {
    console.log('getUserMedia() got stream: ', stream);
    window.stream = stream;
    if (window.URL) {
        gumVideo.src = window.URL.createObjectURL(stream);
    } else {
        gumVideo.src = stream;
    }
}

function handleError(error) {
    console.log('navigator.getUserMedia error: ', error);
}


if (/Edge\/\d./i.test(navigator.userAgent)) {
    // This is Microsoft Edge
    window.alert('Microsoft Edge');
    navigator.mediaDevices.getUserMedia({
        video: {
            facingMode: "user"
        }
    }).then(function (stream) {
        var video = document.getElementById('gum');
        video.srcObject = stream;
        var mediaRecorder = new MediaRecorder(stream);
    }).catch(function (error) {
        console.log(error.name + ": " + error.message);
        handleSuccess();
    });
}

else {
    navigator.mediaDevices.getUserMedia(constraints).then(handleSuccess).catch(handleError);
}


function handleSourceOpen(event) {
    console.log('MediaSource opened');
    sourceBuffer = mediaSource.addSourceBuffer('video/webm; codecs="vp8"');
    console.log('Source buffer: ', sourceBuffer);
}

// recordedVideo.addEventListener('error', function(ev) {
//   console.error('MediaRecording.recordedMedia.error()');
//   alert('Your browser can not play\n\n' + recordedVideo.src
//     + '\n\n media clip. event: ' + JSON.stringify(ev));
// }, true);

function handleDataAvailable(event) {
    if (event.data && event.data.size > 0) {
        recordedBlobs.push(event.data);
    }
}

function handleStop(event) {
    console.log('Recorder stopped: ', event);
}


function sleep(milliseconds) {
    var start = new Date().getTime();
    for (var i = 0; i < 1e7; i++) {
        if ((new Date().getTime() - start) > milliseconds) {
            break;
        }
    }
}


function toggleRecording() {
    if (recordButton.textContent === 'Start Recording' || recordButton.textContent === "Try Again") {
        startRecording();
        document.getElementById("count").style.fontSize = "80px";
    } else {
        stopRecording();
        recordButton.textContent = 'Try Again';
        // playButton.disabled = false;
        downloadButton.disabled = false;
    }
}

// The nested try blocks will be simplified when Chrome 47 moves to Stable
function startRecording() {
    recordButton.textContent = 'Stop Recording';
    $("#custom-message").text("Recording starts in ..");
    $("#count").text(5);
    $("#custom-message").show();
    $("#count").show();
    var counter = 5;
    var interval = setInterval(function () {
        counter--;
        if (recordButton.textContent == "Try Again") {
            clearInterval(interval);
            $("#custom-message").hide();
            $("#count").hide();
        }
        if (counter >= 1) {
            $("#count").text(counter);
        }
        if (counter == 0) {
            document.getElementById("count").style.fontSize = "50px";
            $("#custom-message").text('recording started..');
            $("#count").text('Ask your question');
        }
        if (counter == -2) {
            $("#custom-message").hide();
            $("#count").hide();
            clearInterval(interval);
            recordedBlobs = [];
            var options = {mimeType: 'video/webm;codecs=vp9'};
            if (!MediaRecorder.isTypeSupported(options.mimeType)) {
                console.log(options.mimeType + ' is not Supported');
                options = {mimeType: 'video/webm;codecs=vp8'};
                if (!MediaRecorder.isTypeSupported(options.mimeType)) {
                    console.log(options.mimeType + ' is not Supported');
                    options = {mimeType: 'video/webm'};
                    if (!MediaRecorder.isTypeSupported(options.mimeType)) {
                        console.log(options.mimeType + ' is not Supported');
                        options = {mimeType: ''};
                    }
                }
            }
            try {
                mediaRecorder = new MediaRecorder(window.stream, options);
            } catch (e) {
                console.error('Exception while creating MediaRecorder: ' + e);
                alert('Exception while creating MediaRecorder: '
                    + e + '. mimeType: ' + options.mimeType);
                return;
            }
            console.log('Created MediaRecorder', mediaRecorder, 'with options', options);
            // playButton.disabled = true;
            downloadButton.disabled = true;
            mediaRecorder.onstop = handleStop;
            mediaRecorder.ondataavailable = handleDataAvailable;
            mediaRecorder.start(10); // collect 10ms of data
            console.log('MediaRecorder started', mediaRecorder);
        }
    }, 250);


}

function stopRecording() {
    if (mediaRecorder === undefined || mediaRecorder.state == "inactive") {
        console.log('Not record');
    }
    else {
        mediaRecorder.stop();
        console.log('Recorded Blobs: ', recordedBlobs);
    }
    $("#custom-message").hide();
    $("#count").hide();

    // recordedVideo.controls = true;
}

// function play() {
//   var superBuffer = new Blob(recordedBlobs, {type: 'video/webm'});
//   recordedVideo.src = window.URL.createObjectURL(superBuffer);
// }

function download() {
    var blob = new Blob(recordedBlobs, {type: 'video/webm'});
    var url = window.URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    a.download = 'test.webm';
    document.body.appendChild(a);
    a.click();
    setTimeout(function () {
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    }, 100);
}



