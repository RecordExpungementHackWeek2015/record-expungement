#ifndef MAINTASK_H
#define MAINTASK_H

#include <QObject>

class MainTask : public QObject
{
    Q_OBJECT
public:
    explicit MainTask(QObject *parent = 0);

public slots:
    void run();
    void runList(const QString &input);
    void runFill(const QString &input, const QString &output);
    static void fail(const QString &reason);
};

#endif // MAINTASK_H
