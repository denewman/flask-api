drop table if exists subscription;
drop table if exists destinationGroup;
drop table if exists sensor;
drop table if exists sensorPath;
drop table if exists linkSensorPath;
drop table if exists policy;
drop table if exists policyGroup;
drop table if exists policyPath;
drop table if exists linkPolicyPath;
drop table if exists collector;
drop table if exists router;
drop table if exists linkPolicyRouter;
drop table if exists linkSubscriptionRouter;


create table subscription (
    subscriptionName text not null,
    subscriptionInterval double not null,
    destinationGroupName text not null,
    sensorName text not null,
    PRIMARY KEY(subscriptionName)
    FOREIGN KEY(destinationGroupName) REFERENCES destinationGroup(destinationGroupName),
    FOREIGN KEY(sensorName) REFERENCES sensor(sensorName)
);

create table destinationGroup (
    destinationGroupName text not null,
    destinationGroupAddress text not null,
    destinationGroupPort text not null,
    destinationGroupEncoding text not null,
    destinationGroupProtocol text not null,
    PRIMARY KEY(destinationGroupName)
);

create table sensor (
    sensorName text not null,
    PRIMARY KEY(sensorName)
);

create table sensorPath (
    sensorPathName text not null,
    sensorPath text not null,
    PRIMARY KEY(sensorPathName)
);

create table linkSensorPath (
    sensorName text not null,
    sensorPathName text not null,
    PRIMARY KEY(sensorName, sensorPathName)
);

create table policyGroup (
    policyGroupName text not null,
    collectorName text not null,
    policyName text not null,
    PRIMARY KEY(policyGroupName)
);

create table policy (
    policyName text not null,
    policyDescription text not null,
    policyComment text,
    policyIdentifier text not null,
    policyPeriod double not null,
    PRIMARY KEY(policyName)
);

create table policyPath (
    policyPathName text not null,
    policyPah text not null,
    PRIMARY KEY(policyPathName)
);

create table linkPolicyPath (
    policyName text not null,
    policyPathName text not null,
    PRIMARY KEY(policyName, policyPathName),
    FOREIGN KEY(policyName) REFERENCES policy(policyName),
    FOREIGN KEY(policyPathName) REFERENCES policyPath(policyPathName)
);

create table collector (
    collectorName text not null,
    collectorAddress text not null,
    collectorPort text not null,
    collectorEncoding text not null,
    collectorProtocol text not null,
    PRIMARY KEY(collectorName)
);

create table router (
    routerName text not null,
    routerAddress text not null,
    PRIMARY KEY(routerName)
);

create table linkPolicyRouter (
    policyName text not null,
    routerName text not null,
    PRIMARY KEY(policyName, routerName),
    FOREIGN KEY(policyName) REFERENCES policy(policyName),
    FOREIGN KEY(routerName) REFERENCES router(routerName)
);

create table linkSubscriptionRouter (
    subscriptionName text not null,
    routerName text not null,
    PRIMARY KEY(subscriptionName, routerName),
    FOREIGN KEY(subscriptionName) REFERENCES subscription(subscriptionName),
    FOREIGN KEY(routerName) REFERENCES router(routerName)
);
