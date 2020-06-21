# Angry Chair Release monitor

## Overview
This is a lambda that notifies you whenever the shop.angrychairbrewing.com release page changes.

## Prerequisites
- S3 Bucket for storing the previous copy of the page
- SNS target so that you can notify users
- a precreated s3 file so that it has something to pull
