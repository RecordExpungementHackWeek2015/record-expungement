#ifndef FORMFILLER_H
#define FORMFILLER_H

#include <QObject>
#include <QList>
#include <QMap>

#include <poppler-qt4.h>

#include "fieldinfo.h"

class FormFiller : public QObject
{
    Q_OBJECT
public:
    explicit FormFiller(QString fileName, QObject *parent = 0);

    QList<FieldInfo *> listFieldsInfo();
    void fill(const QMap<QString, FieldInfo*> &fieldsInfo);
    void save(const QString &fileName);

signals:

public slots:

private:
    QString fileName;
    Poppler::Document *document;
};

#endif // FORMFILLER_H
