/****************************************************************************
** Meta object code from reading C++ file 'maintask.h'
**
** Created by: The Qt Meta Object Compiler version 63 (Qt 4.8.6)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include "../pdf-form-filler/maintask.h"
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'maintask.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 63
#error "This file was generated using the moc from 4.8.6. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
static const uint qt_meta_data_MainTask[] = {

 // content:
       6,       // revision
       0,       // classname
       0,    0, // classinfo
       4,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       0,       // signalCount

 // slots: signature, parameters, type, tag, flags
       9,   15,   15,   15, 0x0a,
      16,   33,   15,   15, 0x0a,
      39,   64,   15,   15, 0x0a,
      77,   91,   15,   15, 0x0a,

       0        // eod
};

static const char qt_meta_stringdata_MainTask[] = {
    "MainTask\0run()\0\0runList(QString)\0input\0"
    "runFill(QString,QString)\0input,output\0"
    "fail(QString)\0reason\0"
};

void MainTask::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        Q_ASSERT(staticMetaObject.cast(_o));
        MainTask *_t = static_cast<MainTask *>(_o);
        switch (_id) {
        case 0: _t->run(); break;
        case 1: _t->runList((*reinterpret_cast< const QString(*)>(_a[1]))); break;
        case 2: _t->runFill((*reinterpret_cast< const QString(*)>(_a[1])),(*reinterpret_cast< const QString(*)>(_a[2]))); break;
        case 3: _t->fail((*reinterpret_cast< const QString(*)>(_a[1]))); break;
        default: ;
        }
    }
}

const QMetaObjectExtraData MainTask::staticMetaObjectExtraData = {
    0,  qt_static_metacall 
};

const QMetaObject MainTask::staticMetaObject = {
    { &QObject::staticMetaObject, qt_meta_stringdata_MainTask,
      qt_meta_data_MainTask, &staticMetaObjectExtraData }
};

#ifdef Q_NO_DATA_RELOCATION
const QMetaObject &MainTask::getStaticMetaObject() { return staticMetaObject; }
#endif //Q_NO_DATA_RELOCATION

const QMetaObject *MainTask::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->metaObject : &staticMetaObject;
}

void *MainTask::qt_metacast(const char *_clname)
{
    if (!_clname) return 0;
    if (!strcmp(_clname, qt_meta_stringdata_MainTask))
        return static_cast<void*>(const_cast< MainTask*>(this));
    return QObject::qt_metacast(_clname);
}

int MainTask::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QObject::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 4)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 4;
    }
    return _id;
}
QT_END_MOC_NAMESPACE
