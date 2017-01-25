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
var saveButton = document.querySelector('button#save');
// var playButton = document.querySelector('button#play');
var downloadButton = document.querySelector('button#download');
recordButton.onclick = toggleRecording;
saveButton.onclick = save;
// playButton.onclick = play;
downloadButton.onclick = download;

var h1 = document.getElementsByTagName('h1')[0],
    seconds = 0, minutes = 0, hours = 0,
    t;

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
var videoSelect = document.querySelector('select#videoSource');
var selectors = [videoSelect];
var videoElement = document.getElementById('gum');

function gotDevices(deviceInfos) {
    // Handles being called several times to update labels. Preserve values.
    var values = selectors.map(function(select) {
        return select.value;
    });
    selectors.forEach(function(select) {
        while (select.firstChild) {
            select.removeChild(select.firstChild);
        }
    });

    for (var i = 0; i !== deviceInfos.length; ++i) {
        var deviceInfo = deviceInfos[i];
        var option = document.createElement('option');
        option.value = deviceInfo.deviceId;
        if (deviceInfo.kind === 'videoinput') {
            option.text = deviceInfo.label || 'camera ' + (videoSelect.length + 1);
            videoSelect.appendChild(option);
        } else {
            console.log('Some other kind of source/device: ', deviceInfo);
        }
    }

    selectors.forEach(function(select, selectorIndex) {
        if (Array.prototype.slice.call(select.childNodes).some(function(n) {
            return n.value === values[selectorIndex];
        })) {
            select.value = values[selectorIndex];
        }
    });
}

navigator.mediaDevices.enumerateDevices().then(gotDevices).catch(handleError);

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

function gotStream(stream) {
    window.stream = stream; // make stream available to console
    videoElement.srcObject = stream;
    // Refresh button list in case labels have become available
    return navigator.mediaDevices.enumerateDevices();
}

function start() {
    var videoSource = videoSelect.value;

    var constraints = {
        audio: true,
        video: {facingMode: "environment", deviceId: videoSource ? {exact: videoSource} : undefined}
    };

    if (window.stream) {
        window.stream.getTracks().forEach(function(track) {
            track.stop();
        });
    }

    if (/Edge\/\d./i.test(navigator.userAgent)) {
        // This is Microsoft Edge
        navigator.mediaDevices.getUserMedia({
            video: {
                facingMode: "user",
                audio: true
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
        navigator.mediaDevices.getUserMedia(constraints).then(gotStream).then(handleSuccess).catch(handleError);
    }
}

videoSelect.onchange = start;
start();

function handleSourceOpen(event) {
    console.log('MediaSource opened');
    sourceBuffer = mediaSource.addSourceBuffer('video/webm; codecs="vp8"');
    console.log('Source buffer: ', sourceBuffer);
}


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
    $("#count-replace").hide();
    if (recordButton.textContent === 'Start Recording' || recordButton.textContent === "Try Again") {
        $("#record").css('background-color', '#fe5919');
        $("#save").hide();
        document.getElementById("gum").style.filter = "invert(0)";
        startRecording();
    } else {
        stopRecording();
        clearTimeout(t);
        recordButton.textContent = 'Try Again';
        // playButton.disabled = false;
        downloadButton.disabled = false;
        $("#count-replace").hide();
    }
}

// The nested try blocks will be simplified when Chrome 47 moves to Stable
function startRecording() {
    recordButton.textContent = 'Stop Recording';
    $("#custom-message").text("Recording starts in ..");
    h1.textContent = "00:00:00";
    seconds = 0;
    minutes = 0;
    hours = 0;
    document.getElementById("gum").style.filter = "invert(0.18)";
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
            $("#count-replace").hide();
        }
        if (counter >= 1) {
            $("#count").text(counter);
            $("#count-replace").hide();
        }
        if (counter == 0) {
            $("#count-replace").show();
            $("#custom-message").text('recording started..');
            $("#count").hide();
            if (recordButton.textContent == "Try Again") {
                $("#count-replace").hide();
                $("#custom-message").hide();
            }
        }
        if (counter == -1) {
            $("#count-replace").hide();
            $("#custom-message").hide();

        }
        if (counter == -2) {
            document.getElementById("gum").style.filter = "invert(0)";
            $("#custom-message").hide();
            $("#count-replace").hide();
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
                timer();
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
    }, 750);


}

function stopRecording() {
    document.getElementById("gum").style.filter = "invert(0)";
    if (mediaRecorder === undefined || mediaRecorder.state == "inactive") {
        console.log('Not record');
    }
    else {
        $("#save").show();
        $("#record").css('background-color', '#808080');
        mediaRecorder.stop();
        console.log('Recorded Blobs: ', recordedBlobs);
    }
    $("#custom-message").hide();
    $("#count").hide();
    $("#count-replace").hide();

    // recordedVideo.controls = true;
}


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
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function add() {
    seconds++;
    if (seconds >= 60) {
        seconds = 0;
        minutes++;
        if (minutes >= 60) {
            minutes = 0;
            hours++;
        }
    }
    h1.textContent = (hours ? (hours > 9 ? hours : "0" + hours) : "00") + ":" + (minutes ? (minutes > 9 ? minutes : "0" + minutes) : "00") + ":" + (seconds > 9 ? seconds : "0" + seconds);
    timer();
}

function timer() {
    t = setTimeout(add, 1000);
}

function save() {

    var sizeTheOverlays = function () {
        $(".overlay").resize().each(function () {
            var h = $(this).parent().outerHeight();
            var w = $(this).parent().outerWidth();
            $(this).css("height", h);
            $(this).css("width", w);
        });
    };

    sizeTheOverlays();


    var width = $(window).width();
    $(window).resize(function () {
        if ($(this).width() != width) {
            width = $(this).width();
            sizeTheOverlays();
        }
    });


    var blob = new Blob(recordedBlobs, {type: 'video/webm'});
    var fd = new FormData();
    fd.append('file', 'test1.webm');
    fd.append('data', blob);
    fd.append('interview_question', $("#interview_question").val());

    // Open the connection.
    var csrfcookie = function () {
        var cookieValue = null,
            name = 'csrftoken';
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };

    // $('.overlay').css({opacity: 2});
    var customElement = $("<div>", {
        id: "countdown",
        css: {
            "font-size": "40px",
            "display": "flex",
            "margin-bottom": "20%"
        },
        text: "Video Saving"
    });

    $.LoadingOverlay("show", {
        custom: customElement
    });

    var interview = $("#interview").val();
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/foraliving/video/save/', true);
    xhr.setRequestHeader('X-CSRFToken', csrfcookie());
    xhr.onload = function () {
        if (xhr.status === 200) {
            // $('.overlay').css({opacity: 0});
            $.LoadingOverlay("hide");
            window.location = "/foraliving/question_interview/" + interview + "/";

        } else {
            alert('An error occurred!');
        }
    };
    xhr.send(fd);


}



