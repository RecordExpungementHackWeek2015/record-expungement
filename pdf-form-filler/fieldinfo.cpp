#include "fieldinfo.h"

FieldInfo::FieldInfo(int page, QString type, QString name, QVariant value, QObject *parent) :
    QObject(parent),
    page(page),
    type(type),
    name(name),
    value(value)
{
}

QString FieldInfo::getType() const
{
    return type;
}

void FieldInfo::setType(const QString &value)
{
    type = value;
}

QString FieldInfo::getName() const
{
    return name;
}

void FieldInfo::setName(const QString &value)
{
    name = value;
}

int FieldInfo::getPage() const
{
    return page;
}

void FieldInfo::setPage(int value)
{
    page = value;
}

QVariant FieldInfo::getValue() const
{
    return value;
}

void FieldInfo::setValue(const QVariant &value)
{
    this->value = value;
}
