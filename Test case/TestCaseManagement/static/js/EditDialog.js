
    var dataGrid;
    var organizationTree;

    $(function() {
    	$('#roleIds').combotree({
            url: 'http://192.168.139.213:8080/sklcloudadmin/role/tree.json',
            textFiled : 'roleName',
            multiple: true,
            panelHeight : 'auto',
            panelMaxHeight : 300
        });

    	dataGrid = $('#dataGrid').datagrid({
            url : 'http://192.168.139.213:8080/sklcloudadmin/user/list.json',
            fit : true,
            striped : true,
            rownumbers : true,
            pagination : true,
            singleSelect : true,
            idField : 'id',
            autoRowHeight:false,
            //sortName : 'createTime',
            //sortOrder : 'asc',
            pageSize : 20,
            pageList : [ 10, 20, 30, 40, 50, 100, 200, 300, 400, 500 ],
            columns : [ [ {
                width : '80',
                title : '账号名称',
                field : 'username'
            }, {
                width : '80',
                title : '姓名',
                field : 'realname'
            },{
                width : '130s',
                title : '创建时间',
                field : 'createTime'
            },{
                width : '120',
                title : '工号',
                field : 'jobNumber'
            },{
                width : '120',
                title : '邮箱',
                field : 'email'
            },{
                width : '120',
                title : '手机',
                field : 'mobile'
            },
            {
                width : '200',
                title : '管理员组',
                field : 'rolesList',
                formatter : function(value, row, index) {
                    var roles = [];
                    for(var i = 0; i< value.length; i++) {
                        roles.push(value[i].roleName);
                    }
                    return(roles.join(','));
                }
            }, {
                width : '60',
                title : '账号状态',
                field : 'locked',
                formatter : function(value, row, index) {
                	var str = '';
                	var s = '';
                	if(value){
                		str = '停用';

                		s += $.formatString('<a href="javascript:void(0)"  onclick="changeStatus(\'{0}\');" >'+str+'</a>', row.id);

                	}else{
                		str += '正常';

                		s += $.formatString('<a href="javascript:void(0)"  onclick="changeStatus(\'{0}\');" >'+str+'</a>', row.id);

                	}
                	if(s == ""){
                		return str;
                	}else{
                        return s;
                	}
                }
            } , {
                width : '130s',
                title : '上次登入时间',
                field : 'lastLoginTime'
            },{
                width : '130s',
                title : '上次登出时间',
                field : 'lastLogoutTime'
            },{
                field : 'action',
                title : '操作',
                width : 180,
                formatter : function(value, row, index) {
                    var str = '';

                            str += $.formatString('<a href="javascript:void(0)" class="user-easyui-linkbutton-edit" data-options="plain:true,iconCls:\'icon-edit\'" onclick="editFun(\'{0}\');" >编辑</a>', row.id);

                            str += '&nbsp;|&nbsp;';
                            str += $.formatString('<a href="javascript:void(0)" class="user-easyui-linkbutton-del" data-options="plain:true,iconCls:\'icon-clear\'" onclick="deleteFun(\'{0}\');" >删除</a>', row.id);

                    return str;
                }
            }] ],
            onLoadSuccess:function(data){
                $('.user-easyui-linkbutton-edit').linkbutton({text:'编辑',plain:true,iconCls:'icon-edit'});
                $('.user-easyui-linkbutton-del').linkbutton({text:'删除',plain:true,iconCls:'icon-clear'});
            },
            toolbar : '#toolbar'
        });
    });

    function changeStatus(id){
    	if (id == undefined) {
            var rows = dataGrid.datagrid('getSelections');
            id = rows[0].id;
        } else {
            dataGrid.datagrid('unselectAll').datagrid('uncheckAll');
        }
    	var rows = $("#dataGrid").datagrid('getData').rows;
        var length = rows.length;
        var index;
        for (var i = 0; i < length; i++) {
            if (rows[i]['id'] == id) {
                index = i;
                break;
            }
        }
        var arr=$('#dataGrid').datagrid('getData');
        var locked = arr.rows[index].locked;
        if(locked == true){
        	arr.rows[index].locked = 'false';
        }else{
        	arr.rows[index].locked = 'true';
        }
        //$('#dataGrid').datagrid('refreshRow',index);
        $.post('http://192.168.139.213:8080/sklcloudadmin/user/change.json', {
             id : id
         }, function(result) {
             if (result.success) {
            	 $('#dataGrid').datagrid('reload');
             }else{
            	 parent.$.messager.alert('提示', result.message, 'warning');
             }
         }, 'JSON');
    }

    function addFun() {
        parent.$.modalDialog({
            title : '添加',
            width : 500,
            height : 300,
            href : 'http://192.168.139.213:8080/sklcloudadmin/user/addPage',
            buttons : [ {
                text : '添加',
                handler : function() {
                    parent.$.modalDialog.openner_dataGrid = dataGrid;//因为添加成功之后，需要刷新这个dataGrid，所以先预定义好
                    var f = parent.$.modalDialog.handler.find('#userAddForm');
                    f.submit();
                }
            } ]
        });
    }


    function deleteFun(id) {
        if (id == undefined) {//点击右键菜单才会触发这个
            var rows = dataGrid.datagrid('getSelections');
            id = rows[0].id;
        } else {//点击操作里面的删除图标会触发这个
            dataGrid.datagrid('unselectAll').datagrid('uncheckAll');
        }
        parent.$.messager.confirm('询问', '你是否确认删除当前用户', function(b) {
        	$.extend($.messager.defaults,{
                ok:'messager.defaults.ok',
                cancel:'messager.defaults.cancel'
            });

        	if (b) {
                var currentUserId = '3696240024769711823';/*当前登录用户的ID*/
                if (currentUserId != id) {
                	text : '添加',
                    progressLoad();
                    $.post('http://192.168.139.213:8080/sklcloudadmin/user/delete.json', {
                        id : id
                    }, function(result) {
                        if (result.success) {
                            parent.$.messager.alert('提示', result.message, 'info');
                            dataGrid.datagrid('reload');
                        }else{
                        	parent.$.messager.alert('提示', result.message, 'warning');
                        }
                        progressClose();
                    }, 'JSON');
                } else {
                    parent.$.messager.show({
                        title : '提示',
                        msg : '不能删除自己！'
                    });
                }
            }
        });
    }

    function editFun(id) {
        if (id == undefined) {
            var rows = dataGrid.datagrid('getSelections');
            id = rows[0].id;
        } else {
            dataGrid.datagrid('unselectAll').datagrid('uncheckAll');
        }
        var href = 'http://192.168.139.213:8080/sklcloudadmin/user/editPage?id=' + id;
        parent.$.modalDialog({
            title : '编辑',
            width : 500,
            height : 300,
            href : href,
            buttons : [ {
                text : '确认',
                handler : function() {
                    parent.$.modalDialog.openner_dataGrid = dataGrid;//因为添加成功之后，需要刷新这个dataGrid，所以先预定义好
                    var f = parent.$.modalDialog.handler.find('#userEditForm');
                    f.submit();
                }
            } ]
        });
    }

    function searchFun() {
        dataGrid.datagrid('load', $.serializeObject($('#searchForm')));
    }
    function cleanFun() {
        $('#searchForm input').val('');
        dataGrid.datagrid('load', {});
    }
