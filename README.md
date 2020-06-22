# Angry Chair Release monitor

## Overview
This is a lambda that notifies you whenever the shop.angrychairbrewing.com release page changes.

## Prerequisites
- S3 Bucket for storing the previous copy of the page
- SNS target so that you can notify users
- a precreated s3 file named whatever you have file_name set to
	- TBD: Create this file if it does not exist.
- A role that is allowed to write to S3 and SNS
