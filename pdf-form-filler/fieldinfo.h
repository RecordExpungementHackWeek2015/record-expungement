#ifndef FIELDINFO_H
#define FIELDINFO_H

#include <QObject>
#include <QList>
#include <QVariant>

class FieldInfo : public QObject
{
    Q_OBJECT
public:
    explicit FieldInfo(int page, QString type, QString name, QVariant value = QVariant(), QObject *parent = 0);

    QString getType() const;
    void setType(const QString &value);

    QString getName() const;
    void setName(const QString &value);

    int getPage() const;
    void setPage(int value);

    QVariant getValue() const;
    void setValue(const QVariant &value);

private:
    int page;
    QString type;
    QString name;
    QVariant value;
};

#endif // FIELDINFO_H
