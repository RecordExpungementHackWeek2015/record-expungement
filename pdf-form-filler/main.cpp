#include <QCoreApplication>
#include <QtDebug>
#include <QTimer>
#include <QStringList>

#include "maintask.h"

int main(int argc, char *argv[])
{
    QCoreApplication a(argc, argv);

    QCoreApplication::setApplicationName("pdf-form-filler");
    QCoreApplication::setApplicationVersion("0.1");

    MainTask t;
    QTimer::singleShot(0, &t, SLOT(run()));

    return a.exec();
}
