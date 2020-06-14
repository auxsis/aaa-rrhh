odoo.define('portal_leave_request.leave_request', function (require) {
'use strict';
var core = require('web.core');
var rpc = require('web.rpc');
var session = require('web.session');
var ajax = require('web.ajax');
var _t = core._t;
	$( document ).ready(function() {
	$('.myButton').click(function(e){
		var a = $(this);
                a.addClass('refuse');
                var selected = a.find('.refuse');
                if(selected){
                var leave_request_id=$(this).data('leave')
                var leave_request_date_from=$(this).data('date_from')
                var leave_request_date_to=$(this).data('date_to')
                }
                 var txt;
                  var r = confirm("Are you sure to Cancel the Request? ");
                  if (r == true) {
                          rpc.query({
                        model:'website.leave',
                        method: 'action_cancel',
                        args:[leave_request_id],
                        }).then(function () {

                        window.location = '/leave_cancel';
                        });

                  } else {
                    window.reload();
                  }
		        })
            });
        $(document).on("change", "#date_from", function (){
                    var date1 = document.getElementById("date_from").value;
                    var date2 = document.getElementById("date_to").value;
                    var dateFirst = new Date(date1);
                    var dateSecond = new Date(date2);

		        rpc.query({
                        model:'website.leave',
                        method: 'get_days',
                        args: [date1,date2],
                        }).then(function (result) {
                            duration_id.value =result;
                         });
                         });
           $(document).on("change", "#date_to", function (){
                    var date1 = document.getElementById("date_from").value;
                    var date2 = document.getElementById("date_to").value;
                    var dateFirst = new Date(date1);
                    var dateSecond = new Date(date2);

                rpc.query({
                        model:'website.leave',
                        method: 'get_days',
                        args: [date1,date2],
                        }).then(function (result) {
                            duration_id.value =result ;
                            console.log("result",result)
                         });
                        });
           $(document).on("click", "#half_check", function (){
                    var checkBox = document.getElementById("half_check")
                    var date1 = document.getElementById("date_from").value;
                    var date2 = document.getElementById("date_to").value;
                    if (checkBox.checked == true){
                        request_unit_half_id.style.display = "block";
                        date_to.style.display = "none";
                        label_date_to.style.display ="none";
                        rpc.query({
                        model:'website.leave',
                        method: 'get_days_half',
                        args: [date1,date1],
                        }).then(function (result) {
                            console.log(result)
                            duration_id.value = result;
                         });

                        $("#date_from").on('change', function(){
                            rpc.query({
                        model:'website.leave',
                        method: 'get_days_half',
                        args: [date1,date1],
                        }).then(function (result) {
                            console.log(result)
                             duration_id.value = result;
                         });

                        });
                        }
                    else {
                        
                        request_unit_half_id.style.display = "none";
                        date_to.style.display = "block";
                        label_date_to.style.display = "block";
			            var date1 = document.getElementById("date_from").value;
                        var date2 = document.getElementById("date_to").value;
                        var dateFirst = new Date(date1);
                        var dateSecond = new Date(date2);
			            rpc.query({
                        model:'website.leave',
                        method: 'get_days',
                        args: [date1,date2],
                        }).then(function (result) {
                            duration_id.value =result ;
                         });
                        }
                        });
           $(document).on("click", "#submit_id", function (){
                var checkBox = document.getElementById("half_check")
                if (checkBox.checked == true){
                var date1 = document.getElementById("date_from").value;
                var date2 = document.getElementById("date_from").value;
                }
                else{
                var date1 = document.getElementById("date_from").value;
                var date2 = document.getElementById("date_to").value;
                }
                var dateFirst = new Date(date1);
                var dateSecond = new Date(date2);
                var select_leave = document.getElementById("leave_type_select").value;
                var duration = document.getElementById("duration_id").value;
                var request_unit_half =document.getElementById("request_unit_half_id").value;
                var half_check = $('#half_check').is(":checked");
                var description = document.getElementById("description_id").value;
                var flag =0;
                var check=0;
		        rpc.query({
                        model:'website.leave',
                        method: 'alert_leave_type',
                        args:[select_leave,duration],
                        }).then(function (res) {

                        if (res ==1)
                        {
                         flag=1;
                         alert(_t("The number of remaining leaves is not sufficient for this leave type."));
                        }
                        else
                        {
                        rpc.query({
                        model:'website.leave',
                        method: 'alert_leave',
                        args:[date1,date2,half_check],
                        }).then(function (res) {

                        if (res!=0)
                        {
                        flag=1;
                         alert(_t("You can not have 2 leaves that overlaps on the same day."));
                         }
                        else
                        {
                            ajax.jsonRpc('/request', 'call', {
                                                    'leave_type_select_name' : select_leave,
                                                    'date_from' : date1,
                                                    'date_to' : date2,
                                                    'duration' : duration,
                                                    'half_day' : half_check,
                                                    'description': description,
                                                    'request_unit_half_name': request_unit_half});
                                window.setTimeout(function(){
                                window.location = '/leave_created';

                                        }, 500);
    }
    });
    }
    });
});
});


