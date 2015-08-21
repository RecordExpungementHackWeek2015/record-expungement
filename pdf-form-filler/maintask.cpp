#include "maintask.h"
#include "formfiller.h"

#include <QCoreApplication>
#include <QtDebug>
#include <QTextStream>
#include <QByteArray>
#include <QFile>

#include <qjson/serializer.h>
#include <qjson/parser.h>

#include <unistd.h>
#include <cstdlib>

MainTask::MainTask(QObject *parent) :
    QObject(parent)
{
}

void MainTask::run() {
    QStringList args = QCoreApplication::arguments();
    QString input;
    QString output;

    if (args.size() < 2) {
        fail("No action specified. Actions are \"list\" or \"fill\"");
    }

    QString action = args[1];

    if (action == "list") {
        if (args.size() != 3) {
            fail("Invalid args count. Expected list <input file>");
        }

        input = args[2];

        runList(input);
    } else if (action == "fill") {
        if (args.size() != 4) {
            fail("Invalid args count. Expected fill <input file> <output file>");
        }

        input = args[2];
        output = args[3];

        runFill(input, output);
    } else {
        fail("Action must be \"list\" or \"fill\"");
    }
}

void MainTask::runList(const QString &input)
{
    FormFiller formFiller(input);
    QVariantList output;

    foreach(FieldInfo *info, formFiller.listFieldsInfo()) {
        QVariantMap vInfo;
        vInfo.insert("page", info->getPage());
        vInfo.insert("type", info->getType());
        vInfo.insert("name", info->getName());
        vInfo.insert("value", info->getValue());

        output << vInfo;
    }

    QJson::Serializer serializer;
    QTextStream out(stdout);
    QByteArray json = serializer.serialize(output);

    out << json << endl;

    QCoreApplication::exit();
}

void MainTask::runFill(const QString &input, const QString &output)
{
    QFile inFile;
    inFile.open(stdin, QFile::ReadOnly);

    QByteArray data = inFile.readAll();

    QJson::Parser parser;
    bool ok;

    QVariant inputListRaw = parser.parse(data, &ok);

    if (!ok) {
        fail("Input JSON syntax is invalid");
    }

    if (inputListRaw.type() != QVariant::List) {
        fail("Input JSON is not a list");
    }

    QVariantList inputList = inputListRaw.toList();
    QMap<QString, FieldInfo*> fields;

    foreach (QVariant rawRow, inputList) {
        if (rawRow.type() != QVariant::Map) {
            fail("Invalid JSON row");
        }

        QVariantMap row = rawRow.toMap();

        if (!row.contains("name")
                || !row.contains("page")
                || !row.contains("type")
                || !row.contains("value")) {
            fail("Missing key in row");
        }

        FieldInfo *info = new FieldInfo(
            row["page"].toInt(),
            row["type"].toString(),
            row["name"].toString(),
            row["value"],
            this
        );

        fields[info->getName()] = info;
    }

    FormFiller filler(input);
    filler.fill(fields);
    filler.save(output);

    QCoreApplication::exit();
}

void MainTask::fail(const QString &reason)
{
    qCritical() << reason;
    exit(1);
}
