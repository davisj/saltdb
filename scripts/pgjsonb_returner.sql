-- *** Modified from the upstream https://github.com/saltstack/salt/blob/develop/salt/returners/pgjsonb.py
-- *** Added PK's on the events and returns tables. And a reference from salt_returns.jid to jids.jid.
-- *** Those new PK's allow sqlalchemy reflection which is super sweet.
-- *** Added 'changes' boolean to salt-returns table

-- CREATE DATABASE  salt
--   WITH ENCODING 'utf-8';

--
-- Table structure for table `jids`
--
DROP TABLE IF EXISTS jids;
CREATE TABLE jids (
   jid varchar(255) NOT NULL primary key,
   load jsonb NOT NULL
);
CREATE INDEX idx_jids_jsonb on jids
       USING gin (load)
       WITH (fastupdate=on);

--
-- Table structure for table `salt_returns`
--

DROP TABLE IF EXISTS salt_returns;
DROP SEQUENCE IF EXISTS seq_salt_returns_idx;
CREATE SEQUENCE seq_salt_returns_idx;
CREATE TABLE salt_returns (
  idx integer NOT NULL PRIMARY KEY DEFAULT nextval('seq_salt_returns_idx'),
  fun varchar(50) NOT NULL,
  jid varchar(255) NOT NULL,
  return jsonb NOT NULL,
  id varchar(255) NOT NULL,
  success varchar(10) NOT NULL,
  full_ret jsonb NOT NULL,
  alter_time TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  changes boolean);

CREATE INDEX idx_salt_returns_idx ON salt_returns (idx);
CREATE INDEX idx_salt_returns_id ON salt_returns (id);
CREATE INDEX idx_salt_returns_jid ON salt_returns (jid);
CREATE INDEX idx_salt_returns_fun ON salt_returns (fun);
CREATE INDEX idx_salt_returns_return ON salt_returns
    USING gin (return) with (fastupdate=on);
CREATE INDEX idx_salt_returns_full_ret ON salt_returns
    USING gin (full_ret) with (fastupdate=on);


--
-- Table with pointers to jobs that made changes
--

DROP TABLE IF EXISTS salt_changes;
DROP SEQUENCE IF EXISTS seq_salt_changes_id;
CREATE SEQUENCE seq_salt_changes_id;
CREATE TABLE salt_changes (
    idx integer NOT NULL PRIMARY KEY DEFAULT nextval('seq_salt_changes_id'),
    id varchar(255) NOT NULL,
    jid varchar(255) NOT NULL);
-- alter_time TIMESTAMP WITH TIME ZONE DEFAULT NOW());


--
-- Table structure for table `salt_events`
--

DROP TABLE IF EXISTS salt_events;
DROP SEQUENCE IF EXISTS seq_salt_events_id;
CREATE SEQUENCE seq_salt_events_id;
CREATE TABLE salt_events (
    id BIGINT NOT NULL PRIMARY KEY DEFAULT nextval('seq_salt_events_id'),
    tag varchar(255) NOT NULL,
    data jsonb NOT NULL,
    alter_time TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    master_id varchar(255) NOT NULL);

CREATE INDEX idx_salt_events_tag on
    salt_events (tag);
CREATE INDEX idx_salt_events_data ON salt_events
    USING gin (data) with (fastupdate=on);
