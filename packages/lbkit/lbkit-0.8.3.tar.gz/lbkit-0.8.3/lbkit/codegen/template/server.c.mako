<% from lbkit.codegen.ctype_defination import StringValidator %>\
#include "lb_base.h"
#include "${intf.name}.h"

<%
class_name = intf.alias
properties = "_" + class_name + "_properties"
signal_processer = "_" + class_name + "_signals"
%>\
## 定义结构体ODF加载函数
% for name, stru in intf.structures.items():
/* ${name} structure object */
/* START: 结构体${name}及其数组类型的ODF加载函数 */
struct _${name} *_load_odf_as_${name}(yaml_document_t *doc, yaml_node_t *node);
struct _${name} **_load_odf_as_${name}_v(yaml_document_t *doc, yaml_node_t *node);

% endfor
## 定义枚举ODF加载函数
% for name, enum in intf.enumerations.items():
/* START: 枚举${name}及其数组类型的ODF加载函数 */
${name} _load_odf_as_${name}(yaml_document_t *doc, yaml_node_t *node);
${name} *_load_odf_as_${name}_v(yaml_document_t *doc, yaml_node_t *node, gsize *n);

% endfor
## 定义字典ODF加载函数
% for name, dictionary in intf.dictionaries.items():
/* START: 字典${name}及其数组类型的ODF加载函数 */
${name} *_load_odf_as_${name}(yaml_document_t *doc, yaml_node_t *node);
${name} **_load_odf_as_${name}_v(yaml_document_t *doc, yaml_node_t *node);

% endfor
## 定义结构体ODF加载函数
% for name, stru in intf.structures.items():
/* ${name} structure object */
/* START: 结构体${name}及其数组类型的ODF加载函数 */
struct _${name} *_load_odf_as_${name}(yaml_document_t *doc, yaml_node_t *node)
{
<% cnt = 0 %>\
    % for prop in stru.values.parameters:
        % if prop.odf_load_func() is not None:
<% cnt = cnt + 1 %>\
        % endif
    % endfor
% if cnt == 0:
    return g_new0(struct _${name}, 1);
% else:
    __unused yaml_node_t *val;
    struct _${name} *output = g_new0(struct _${name}, 1);
    GHashTable *prop_table = load_yaml_mapping_to_hash_table(doc, node);
    % for prop in stru.values.parameters:
        % if prop.odf_load_func() is not None:
    /* process ${prop.name} */
    val = g_hash_table_lookup(prop_table, "${prop.name}");
    if (val)
        ${prop.odf_load_func().replace("n_<arg_name>", "output->n_" + prop.name).replace("<arg_name>", "output->" + prop.name).replace("<node>", "val")};
        % endif
    % endfor

    g_hash_table_destroy(prop_table);
    return output;
% endif
}

struct _${name} **_load_odf_as_${name}_v(yaml_document_t *doc, yaml_node_t *node)
{
    yaml_node_t *val;
    gint i = 0;
    if (node->type != YAML_SEQUENCE_NODE) {
        log_warn("Load array ${name} failed because node type error, need type 1(sequence), get type %d", node->type);
        return g_new0(struct _${name} *, 1);
    }
    yaml_node_item_t *top = node->data.sequence.items.top;
    yaml_node_item_t *start = node->data.sequence.items.start;
    gsize cnt = ((gsize)top - (gsize)start) / sizeof(yaml_node_item_t);
    struct _${name} **output = g_new0(struct _${name} *, cnt + 1);

    for (yaml_node_item_t *item = start; item < top; item++) {
        val = yaml_document_get_node(doc, *item);
        output[i++] = _load_odf_as_${name}(doc, val);
    }
    return output;
}

% endfor
## 定义枚举ODF加载函数
% for name, enum in intf.enumerations.items():
${name} _load_odf_as_${name}(yaml_document_t *doc, yaml_node_t *node)
{
% if codegen_version.be("5.0"):
    g_assert(node->type == YAML_SCALAR_NODE);
    if (node->type != YAML_SCALAR_NODE) {
        return _${name}_Invalid;
    }

    for (int i = 0; i <= ${len(enum.values.parameters)}; i++) {
        if (g_strcmp0((const gchar *)node->data.scalar.value, ${name}_as_string(i)) == 0) {
            return (${name})i;
        }
    }
    return _${name}_Invalid;
% else:
    g_assert(node->type == YAML_SCALAR_NODE);
    if (node->type != YAML_SCALAR_NODE) {
        return _${name}Invalid;
    }

    for (int i = 0; i <= ${len(enum.values.parameters)}; i++) {
        if (g_strcmp0((const gchar *)node->data.scalar.value, ${name}_as_string(i)) == 0) {
            return (${name})i;
        }
    }
    return _${name}Invalid;
% endif
}

${name} *_load_odf_as_${name}_v(yaml_document_t *doc, yaml_node_t *node, gsize *n)
{
    g_assert(doc && node && n);
    yaml_node_t *val;
    gint i = 0;
    if (node->type != YAML_SEQUENCE_NODE) {
        log_warn("Load array ${name} failed because node type error, need type 1(sequence), get type %d", node->type);
        return g_new0(${name}, 1);
    }
    yaml_node_item_t *top = node->data.sequence.items.top;
    yaml_node_item_t *start = node->data.sequence.items.start;
    *n = ((gsize)top - (gsize)start) / sizeof(yaml_node_item_t);
    ${name} *output = g_new0(${name}, *n);

    for (yaml_node_item_t *item = start; item < top; item++) {
        val = yaml_document_get_node(doc, *item);
        output[i++] = _load_odf_as_${name}(doc, val);
    }
    return output;
}

% endfor
## 定义字典ODF加载函数
% for name, dictionary in intf.dictionaries.items():
${name} *_load_odf_as_${name}(yaml_document_t *doc, yaml_node_t *node)
{
    GHashTable *prop_table = NULL;
    yaml_node_t *val = NULL;
    ${name} *dict = ${name}_new();
    yaml_node_item_t *top = node->data.sequence.items.top;
    yaml_node_item_t *start = node->data.sequence.items.start;
    for (yaml_node_item_t *item = start; item < top; item++) {
        val = yaml_document_get_node(doc, *item);
        ## 转换成hash表以获取key和properties
        prop_table = load_yaml_mapping_to_hash_table(doc, val);
        yaml_node_t *key = g_hash_table_lookup(prop_table, "key");
        yaml_node_t *properties = g_hash_table_lookup(prop_table, "properties");
        g_hash_table_destroy(prop_table);

        ${", ".join(dictionary.key_obj.declare()).replace("<arg_name>", "key_val").replace("<const>", "")};
        ${dictionary.key_obj.odf_load_func().replace("<arg_name>", "key_val").replace("<node>", "key")};

        ## 创建一个新的字典成员
        ${name}${dictionary.key} *item = g_new0(${name}${dictionary.key}, 1);
        ## 转换成hash表
        prop_table = load_yaml_mapping_to_hash_table(doc, properties);
        ## 迭代所有成员并从odf中还原数据
        % for prop in dictionary.values.parameters:
            % if prop.odf_load_func() is not None:
        val = g_hash_table_lookup(prop_table, "${prop.name}");
        if (val)
            ${prop.odf_load_func().replace("n_<arg_name>", "item->n_" + prop.name).replace("<arg_name>", "item->" + prop.name).replace("<node>", "val")};
            % endif
        % endfor
        g_hash_table_destroy(prop_table);
        dict->insert(dict, key_val, &item);
        % for line in dictionary.key_obj.free_func():
        ${line.replace("<arg_name>", "key_val")};
        % endfor
    }
    return dict;
}

${name} **_load_odf_as_${name}_v(yaml_document_t *doc, yaml_node_t *node)
{
    yaml_node_t *val;
    gint i = 0;
    if (node->type != YAML_SEQUENCE_NODE) {
        log_warn("Load array ${name} failed because node type error, need type 1(sequence), get type %d", node->type);
        return g_new0(${name} *, 1);
    }
    yaml_node_item_t *top = node->data.sequence.items.top;
    yaml_node_item_t *start = node->data.sequence.items.start;
    gsize cnt = ((gsize)top - (gsize)start) / sizeof(yaml_node_item_t);
    ${name} **output = g_new0(${name} *, cnt + 1);

    for (yaml_node_item_t *item = start; item < top; item++) {
        val = yaml_document_get_node(doc, *item);
        output[i++] = _load_odf_as_${name}(doc, val);
    }
    return output;
}

% endfor
static ${class_name}_Properties ${properties};
static const ${class_name}_Signals *${signal_processer} = NULL;

% for prop in intf.properties:
    % if prop.deprecated:
__deprecated void ${class_name}_set_${prop.name}(${class_name} obj,
    ${", ".join(prop.declare()).replace("<arg_name>", "value").replace("<const>", "const ")})
    % else:
void ${class_name}_set_${prop.name}(${class_name} obj,
    ${", ".join(prop.declare()).replace("<arg_name>", "value").replace("<const>", "const ")})
    % endif
{
    GVariant *tmp = NULL;
    % for line in prop.encode_func():
    ${line.replace("<arg_out>", "tmp").replace("n_<arg_name>", "n_value").replace("<arg_name>", "value")};
    % endfor
    lbo_set_memory((LBO *)obj, &_${class_name}_properties.${prop.name}, tmp);
    g_variant_unref(tmp);
}

% endfor
% for signal in intf.signals:
<% REQ_PARA = f'' %>\
    % if len(signal.properties.parameters) > 0:
<% REQ_PARA = f'const {class_name}_{signal.name}_Msg *msg, ' %>\
    % endif
    % if codegen_version.be("5.1"):
        % if signal.deprecated:
__deprecated gboolean ${class_name}_Emit_${signal.name}(${class_name} obj,
    const gchar *destination, ${REQ_PARA}GError **error)
        % else:
gboolean ${class_name}_Emit_${signal.name}(${class_name} obj, const gchar *destination,
    ${REQ_PARA}GError **error)
        % endif
    % else:
        % if signal.deprecated:
__deprecated gboolean ${class_name}_${signal.name}_Signal(${class_name} obj,
    const gchar *destination, ${REQ_PARA}GError **error)
        % else:
gboolean ${class_name}_${signal.name}_Signal(${class_name} obj, const gchar *destination,
    ${REQ_PARA}GError **error)
        % endif
    % endif
{
    if (error == NULL) {
        log_error("Emit ${signal.name} with parameter error, error is NULL");
        return FALSE;
    }
    if (obj == NULL) {
        *error = g_error_new(G_DBUS_ERROR, G_DBUS_ERROR_FAILED, "Emit ${signal.name} with parameter error, obj is NULL");
        return FALSE;
    }
    % if len(signal.properties.parameters) == 0:
    void *msg = NULL;
    % endif
    return lb_impl.emit_signal((LBO *)obj, destination,
        (const LBSignal *)&${signal_processer}->${signal.name}, msg, error);
}

% endfor
static LBO *_${class_name}_create(const gchar *obj_name, gpointer opaque);
static void _${class_name}_destroy(LBO *obj);
static void _load_from_odf(yaml_document_t *doc, yaml_node_t *node, LBO *obj,
    lbo_property_reference_loaded_handler ref_loaded, gpointer user_data);

static LBInterface _${class_name}_interface = {
    .create = _${intf.alias}_create,
    .destroy = _${class_name}_destroy,
    .validate_odf = ${intf.name.replace(".", "_")}_validate_odf,
    .load_from_odf = _load_from_odf,
    .is_remote = 0,
    .name = "${intf.name}",
    .properties = (LBProperty *)&${properties},
    .interface = NULL,  /* load from usr/share/dbus-1/interfaces/${intf.name} by lb_init */
};

% for prop in intf.properties:
static void _load_odf_as_prop_${prop.name}(yaml_document_t *doc, GHashTable *prop_table,
    struct _${class_name} *obj, lbo_property_reference_loaded_handler ref_loaded, gpointer user_data)
{
    __unused gint i = 0;
    const gchar *flags = NULL;
    yaml_node_t *val = g_hash_table_lookup(prop_table, "_${prop.name}_flags");
    if (val && val->type == YAML_SCALAR_NODE) {
        flags = (const gchar *)val->data.scalar.value;
    }
    val = g_hash_table_lookup(prop_table, "${prop.name}");
    ## validate接口在加载odf前完成属性是否必选校验，此处如果是必选属性一定存在
    if (!val) {
        ## 设置默认值
        % if prop.default:
            % if prop.ctype == "boolean":
                % if prop.default:
        obj->${prop.name} = TRUE;
                % endif
            % elif prop.ctype in ["byte", "int16", "uint16", "int32", "uint32", "int64", "uint64", "size", "ssize", "double"]:
                    % if prop.ctype == "uint64":
        obj->${prop.name} = ${prop.default}UL;
                    % elif prop.ctype == "int64":
        obj->${prop.name} = ${prop.default}LL;
                    % else:
        obj->${prop.name} = ${prop.default};
                    % endif
            % elif prop.ctype in ["object_path", "string", "signature"]:
        obj->${prop.name} = g_strdup("${prop.default}");
            % elif prop.ctype == "array[boolean]":
        i = 0;
        obj->n_${prop.name} = ${len(prop.default)};
        obj->${prop.name} = g_new0(gboolean, obj->n_${prop.name});
                % for val in prop.default:
                    % if val:
        obj->${prop.name}[i++] = TRUE;
                    % else:
        obj->${prop.name}[i++] = FALSE;
                    % endif
                % endfor
            % elif prop.ctype in ["array[byte]", "array[int16]", "array[uint16]", "array[int32]", "array[uint32]", "array[int64]", "array[uint64]", "array[size]", "array[ssize]", "array[double]"]:
<% ctype = prop.ctype[6:-1]%>
        i = 0;
        obj->n_${prop.name} = ${len(prop.default)};
        obj->${prop.name} = g_new0(g${ctype},  obj->n_${prop.name});
                % for val in prop.default:
                    % if prop.ctype == "array[uint64]":
        obj->${prop.name}[i++] = ${val}UL;
                    % elif prop.ctype == "array[int64]":
        obj->${prop.name}[i++] = ${val}LL;
                    % else:
        obj->${prop.name}[i++] = ${val};
                    % endif
                % endfor
            % elif prop.ctype in ["array[object_path]", "array[string]", "array[signature]"]:
        i = 0;
        obj->${prop.name} = g_new0(gchar *, ${len(prop.default) + 1});
                % for val in prop.default:
        obj->${prop.name}[i++] = g_strdup("${val}");
                % endfor
            % endif
        % endif
        if (flags) {
            ## 属性不存在时传入的value为空，需要开发者在回调函数中完成异常（有flags无属性值）处理
            ref_loaded(obj, &${properties}.${prop.name}, doc, NULL, user_data, flags);
        }
        return;
    }
    % if "refobj" in prop.flags:
    ref_loaded(obj, &${properties}.${prop.name}, doc, val, user_data, flags);
    % else:
    const gchar *val_str  = (const gchar *)val->data.scalar.value;
    if (val->type == YAML_SCALAR_NODE && val_str[0] == '$' &&
        g_regex_match(lb_ref_prop_regex(), val_str, 0, NULL)) {
        ref_loaded(obj, &${properties}.${prop.name}, doc, val, user_data, flags);
    } else {
        % if prop.odf_load_func() is not None:
        ${prop.odf_load_func().replace("n_<arg_name>", "obj->n_" + prop.name).replace("<arg_name>", "obj->" + prop.name).replace("<node>", "val")};
        % endif
        if (flags) {
            ref_loaded(obj, &${properties}.${prop.name}, NULL, NULL, user_data, flags);
        }
    }
    % endif
}

% endfor

static LBBase *_get_real_object(LBO *obj)
{
    LBBase *real = (LBBase *)strstr((const char *)obj, LB_MAGIC);
    if ((gconstpointer)real != (gconstpointer)obj) {
        log_error("Get real object fail, Perhaps the memory has been freed, call abort() now");
        abort();
    }
    return real;
}

static void _load_from_odf(yaml_document_t *doc, yaml_node_t *node, LBO *obj,
    lbo_property_reference_loaded_handler ref_loaded, gpointer user_data)
{
    g_assert(doc && node && obj);
    if (!obj) {
        return;
    }
<% cnt = 0 %>\
    % for prop in intf.properties:
        % if prop.odf_load_func() is not None:
<% cnt = cnt + 1 %>\
        % endif
    % endfor
% if cnt == 0:
    return;
% else:
    struct _${class_name} *real_obj = (struct _${class_name} *)_get_real_object(obj);
    ${class_name}_clean(real_obj);
    GHashTable *prop_table = load_yaml_mapping_to_hash_table(doc, node);
    % for prop in intf.properties:
    _load_odf_as_prop_${prop.name}(doc, prop_table, real_obj, ref_loaded, user_data);
    % endfor

    g_hash_table_destroy(prop_table);
% endif
}

/**
 * @brief 销毁对象
 *
 * @param obj 待销毁的对象句柄
 */
static void _${class_name}_destroy(LBO *obj)
{
    g_assert(obj);
    struct _${class_name} *real_obj = (struct _${class_name} *)_get_real_object(obj);
    g_rec_mutex_clear(real_obj->_base.lock);
    g_free(real_obj->_base.lock);
    ${class_name}_clean(real_obj);
    memset(real_obj, 0, sizeof(struct _${class_name}));
    g_free(real_obj);
}

/**
 * @brief 分配对象
 *
 * @param obj_name 对象名，需要由调用者分配内存
 * @param opaque 上层应用需要写入对象的用户数据，由上层应用使用
 */
static LBO *_${class_name}_create(const gchar *obj_name, gpointer opaque)
{
    __unused gint i = 0;
    struct _${class_name} *obj = g_new0(struct _${class_name}, 1);
    memcpy(obj->_base.magic, LB_MAGIC, strlen(LB_MAGIC) + 1);
    obj->_base.lock = g_new0(GRecMutex, 1);
    g_rec_mutex_init(obj->_base.lock);
    obj->_base.name = obj_name;
    obj->_base.intf = &_${class_name}_interface;
    obj->_base.opaque = opaque;
    % for prop in intf.properties:
        % if prop.default:
            % if prop.ctype == "boolean":
                % if prop.default:
    obj->${prop.name} = TRUE;
                % endif
            % elif prop.ctype in ["byte", "int16", "uint16", "int32", "uint32", "int64", "uint64", "size", "ssize", "double"]:
                    % if prop.ctype == "uint64":
    obj->${prop.name} = ${prop.default}UL;
                    % elif prop.ctype == "int64":
    obj->${prop.name} = ${prop.default}LL;
                    % else:
    obj->${prop.name} = ${prop.default};
                    % endif
            % elif prop.ctype in ["object_path", "string", "signature"]:
    obj->${prop.name} = g_strdup("${prop.default}");
            % elif prop.ctype == "array[boolean]":
    i = 0;
    obj->n_${prop.name} = ${len(prop.default)};
    obj->${prop.name} = g_new0(gboolean, obj->n_${prop.name});
                % for val in prop.default:
                    % if val:
    obj->${prop.name}[i++] = TRUE;
                    % else:
    obj->${prop.name}[i++] = FALSE;
                    % endif
                % endfor
            % elif prop.ctype in ["array[byte]", "array[int16]", "array[uint16]", "array[int32]", "array[uint32]", "array[int64]", "array[uint64]", "array[size]", "array[ssize]", "array[double]"]:
<% ctype = prop.ctype[6:-1]%>
    i = 0;
    obj->n_${prop.name} = ${len(prop.default)};
    obj->${prop.name} = g_new0(g${ctype},  obj->n_${prop.name});
                % for val in prop.default:
                    % if prop.ctype == "array[uint64]":
    obj->${prop.name}[i++] = ${val}UL;
                    % elif prop.ctype == "array[int64]":
    obj->${prop.name}[i++] = ${val}LL;
                    % else:
    obj->${prop.name}[i++] = ${val};
                    % endif
                % endfor
            % elif prop.ctype in ["array[object_path]", "array[string]", "array[signature]"]:
    i = 0;
    obj->${prop.name} = g_new0(gchar *, ${len(prop.default) + 1});
                % for val in prop.default:
    obj->${prop.name}[i++] = g_strdup("${val}");
                % endfor
            % endif
        % endif
    % endfor
    return (LBO *)obj;
}

LBInterface *${class_name}_interface(void)
{
    return &_${class_name}_interface;
}

${class_name}_Properties *${class_name}_properties(void)
{
    return &${properties};
}

% if codegen_version.be("4.0"):
${class_name} ${class_name}_get(const gchar *name)
{
    return lb_impl._get(&_${class_name}_interface, name);
}

${class_name} ${class_name}_new(const gchar *name, gboolean *exist)
{
    LBO *obj = lb_impl._new(&_${class_name}_interface, name, exist);
    return (${class_name} )obj;
}

void ${class_name}_unref(${class_name} *obj)
{
    lb_impl._unref((LBO **)obj);
}

/* 加对象引用计数 */
${class_name} ${class_name}_ref(${class_name} obj)
{
    return (${class_name} )lb_impl._ref((LBO *)obj);
}

/* 设置在位状态 */
void ${class_name}_present_set(${class_name} obj, gboolean present)
{
    lb_impl._present_set((LBO *)obj, present);
}

/* 获取在位状态 */
gboolean ${class_name}_present(${class_name} obj)
{
    return lb_impl._present((LBO *)obj);
}

/* 绑定数据 */
void ${class_name}_bind(${class_name} obj, gpointer data, GDestroyNotify destroy_func)
{
    lb_impl._bind((LBO *)obj, data, destroy_func);
}

/* 获取绑定数据 */
gpointer ${class_name}_data(${class_name} obj)
{
    return lb_impl._data((LBO *)obj);
}

/* @notes 属性对象属性值变更(后)事件 */
gint ${class_name}_on_prop_changed(${class_name} obj, const gchar *prop, ${class_name}_after_changed_hook pc, gpointer user_data, GDestroyNotify destroy)
{
    return lb_impl._on_prop_changed((LBO *)obj, prop, (lbo_after_changed_hook)pc, user_data, destroy);
}

/* 取消监听，成功取消监听时会调用监听时设置的destroy回调清除注册时的user_data */
void ${class_name}_on_prop_changed_cancel(${class_name} obj, const gchar *prop, ${class_name}_after_changed_hook pc, gconstpointer user_data)
{
    lb_impl._on_prop_changed_cancel((LBO *)obj, prop, (lbo_after_changed_hook)pc, user_data);
}

/* 对象变更事件 */
void ${class_name}_on_changed(${class_name}_on_changed_hook cb, gpointer user_data, GDestroyNotify destroy)
{
    lb_impl._on_changed(&_${class_name}_interface, (LbObjectHook)cb, user_data, destroy);
}

/* 注册对象释放回调 */
void ${class_name}_before_destroy(${class_name} obj, GHookFunc cb, gpointer user_data)
{
    lb_impl._before_destroy((LBO *)obj, cb, user_data);
}

/* 查询第n个对象 */
${class_name} ${class_name}_nth(int nth)
{
    return (${class_name} )lb_impl._nth(&_${class_name}_interface, nth);
}

/* 查询对象名称 */
const gchar *${class_name}_name(${class_name} obj)
{
    return lbo_name((LBO *)obj);
}

/* 对象加锁 */
void ${class_name}_lock(${class_name} obj)
{
    lbo_lock((LBO *)obj);
}

/* 对象解锁 */
void ${class_name}_unlock(${class_name} obj)
{
    lbo_unlock((LBO *)obj);
}

/* 对象列表查询接口 */
GSList *${class_name}_list(void)
{
    return lb_impl._list(&_${class_name}_interface);
}

% for prop in intf.properties:
/* 监听属性${prop.name}变更 */
void ${class_name}_${prop.name}_hook(${class_name}_before_change_hook before, ${class_name}_after_changed_hook after, gpointer user_data)
{
    LBPropertyHook hook = {
        .before = (lbo_before_change_hook)before,
        .after = (lbo_after_changed_hook)after,
        .user_data = user_data
    };
    lb_impl._prop_hook(&${properties}.${prop.name}, &hook);
}

% endfor
% endif
static void __constructor(150) ${class_name}_register(void)
{
    // 从公共库中复制信号处理函数
    ${signal_processer} = ${class_name}_signals();
    // 从公共库中复制方法处理函数
    _${class_name}_interface.methods = (LBMethod *)${class_name}_methods();
    _${class_name}_interface.signals = (LBSignal *)${class_name}_signals();

    // 从公共库中复制属性信息
    memcpy(&${properties}, ${class_name}_properties_const(), sizeof(${properties}));
    lb_interface_register(&_${class_name}_interface,
                           "${intf.introspect_xml_sha256}",
                           "/usr/share/dbus-1/interfaces/${intf.name}.xml");
}
